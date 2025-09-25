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

# --- IAM Role & Policy for Scouter Lambda ---
resource "aws_iam_role" "scouter_lambda_role" {
  name = "ad-scouter-scouter-lambda-role"
  assume_role_policy = jsonencode({
    Version   = "2012-10-17",
    Statement = [{
      Action    = "sts:AssumeRole",
      Effect    = "Allow",
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

# DynamoDB Stream 읽기, CloudWatch 로그 쓰기 권한 정책
# TODO: 추후 S3 쓰기, SES 이메일 보내기, Gemini API 호출 권한 추가 필요
resource "aws_iam_policy" "scouter_lambda_policy" {
  name = "ad-scouter-scouter-lambda-policy"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = [
          "dynamodb:DescribeStream",
          "dynamodb:GetRecords",
          "dynamodb:GetShardIterator",
          "dynamodb:ListStreams"
        ],
        Resource = var.dynamodb_stream_arn
      },
      {
        Effect   = "Allow",
        Action   = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "scouter_policy_attachment" {
  role       = aws_iam_role.scouter_lambda_role.name
  policy_arn = aws_iam_policy.scouter_lambda_policy.arn
}

# --- Lambda Function ---
data "archive_file" "scouter_zip" {
  type        = "zip"
  source_dir  = "${path.module}/src"
  output_path = "${path.module}/dist/scouter.zip"
}

resource "aws_lambda_function" "scouter_lambda" {
  function_name    = "ad-scouter-scouter"
  handler          = "scouter.handler"
  runtime          = "python3.11"
  role             = aws_iam_role.scouter_lambda_role.arn
  
  filename         = data.archive_file.scouter_zip.output_path
  source_code_hash = data.archive_file.scouter_zip.output_base64sha256
  timeout          = 300 # 5분
  
  environment {
    variables = {
      GEMINI_API_KEY = var.gemini_api_key
    }
  }
}

# --- Event Source Mapping ---
# DynamoDB 스트림과 Scouter Lambda를 연결합니다.
resource "aws_lambda_event_source_mapping" "dynamodb_mapping" {
  event_source_arn  = var.dynamodb_stream_arn
  function_name     = aws_lambda_function.scouter_lambda.arn
  starting_position = "LATEST"
  batch_size        = 100
}
