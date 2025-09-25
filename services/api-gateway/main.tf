# Terraform 및 AWS Provider 설정
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# --- IAM Role & Policy ---
# Lambda 함수가 실행될 때 필요한 권한을 정의합니다.
resource "aws_iam_role" "lambda_exec_role" {
  name = "ad-scouter-ingest-lambda-exec-role"

  assume_role_policy = jsonencode({
    Version   = "2012-10-17",
    Statement = [{
      Action    = "sts:AssumeRole",
      Effect    = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

# Lambda가 CloudWatch에 로그를 쓸 수 있도록 하는 기본 정책
resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# --- Lambda 함수 아카이브 및 리소스 ---
# Python 소스 코드를 zip 파일로 압축합니다.
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/src"
  output_path = "${path.module}/dist/ingest.zip"
}

# Lambda 함수 리소스를 정의합니다.
resource "aws_lambda_function" "ingest_lambda" {
  function_name    = "ad-scouter-ingest-api"
  handler          = "ingest.handler"
  runtime          = "python3.11"
  role             = aws_iam_role.lambda_exec_role.arn
  
  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  # 15분 타임아웃
  timeout = 900

  # 환경 변수 설정
  environment {
    variables = {
      KINESIS_STREAM_NAME = aws_kinesis_stream.data_stream.name
    }
  }
}

# --- API Gateway (HTTP API) ---
# 비용 효율적인 HTTP API를 생성합니다.
resource "aws_apigatewayv2_api" "http_api" {
  name          = "ad-scouter-http-api"
  protocol_type = "HTTP"
  
  # CORS 설정
  cors_configuration {
    allow_origins = ["*"] # 프로덕션에서는 허용된 도메인 목록으로 변경
    allow_methods = ["POST", "OPTIONS"]
    allow_headers = ["Content-Type"]
  }
}

# API Gateway와 Lambda 함수를 연결합니다.
resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id           = aws_apigatewayv2_api.http_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.ingest_lambda.invoke_arn
}

# /ingest 경로로 오는 POST 요청을 Lambda 통합으로 라우팅합니다.
resource "aws_apigatewayv2_route" "ingest_route" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "POST /ingest"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

# API를 배포하기 위한 기본 스테이지를 생성합니다.
resource "aws_apigatewayv2_stage" "default_stage" {
  api_id      = aws_apigatewayv2_api.http_api.id
  name        = "$default"
  auto_deploy = true
}

# Lambda 함수가 API Gateway로부터 호출될 수 있도록 권한을 부여합니다.
resource "aws_lambda_permission" "api_gw_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ingest_lambda.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.http_api.execution_arn}/*/*"
}

# --- 출력 ---
# 배포된 API의 URL을 출력합니다.
output "api_endpoint_url" {
  description = "The invocation URL for the API Gateway."
  value       = "${aws_apigatewayv2_api.http_api.api_endpoint}/ingest"
}

# --- Kinesis Data Stream ---
# 수집된 이벤트를 실시간으로 처리하기 위한 데이터 스트림을 생성합니다.
resource "aws_kinesis_stream" "data_stream" {
  name        = "ad-scouter-ingest-stream"
  shard_count = 1 # 초기에는 1개의 샤드로 시작, 트래픽에 따라 조정 가능
}

# --- IAM Policy for Kinesis ---
# Lambda 함수가 Kinesis 스트림에 데이터를 쓸(PutRecord) 수 있도록 하는 정책을 정의합니다.
resource "aws_iam_policy" "lambda_kinesis_policy" {
  name        = "ad-scouter-lambda-kinesis-write-policy"
  description = "Allows Lambda function to write to the Kinesis data stream"

  policy = jsonencode({
    Version   = "2012-10-17",
    Statement = [
      {
        Action   = [
          "kinesis:PutRecord",
          "kinesis:PutRecords"
        ],
        Effect   = "Allow",
        Resource = aws_kinesis_stream.data_stream.arn
      }
    ]
  })
}

# 생성한 Kinesis 쓰기 정책을 Lambda 실행 역할(Role)에 연결(Attach)합니다.
resource "aws_iam_role_policy_attachment" "lambda_kinesis_attachment" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = aws_iam_policy.lambda_kinesis_policy.arn
}

# --- 추가 출력 ---
# 생성된 Kinesis 스트림의 이름을 출력합니다.
output "kinesis_stream_name" {
  description = "The name of the Kinesis data stream."
  value       = aws_kinesis_stream.data_stream.name
}
