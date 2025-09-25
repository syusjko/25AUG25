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

# --- DynamoDB Table ---
# 분석된 통계 데이터를 저장할 DynamoDB 테이블을 생성합니다.
resource "aws_dynamodb_table" "stats_table" {
  name           = "ad-scouter-stats"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "customerId"
  range_key      = "eventId"

  attribute {
    name = "customerId"
    type = "S"
  }

  attribute {
    name = "eventId"
    type = "S"
  }

  # DynamoDB 스트림 활성화
  stream_enabled   = true
  stream_view_type = "NEW_AND_OLD_IMAGES" # 변경 전후 데이터를 모두 스트림으로 보냅니다.
}

# --- IAM Role & Policy for Processor Lambda ---
# 데이터 처리 Lambda가 필요한 AWS 서비스(Kinesis, DynamoDB, CloudWatch)에 접근할 수 있는 권한을 정의합니다.
resource "aws_iam_role" "processor_lambda_role" {
  name = "ad-scouter-processor-lambda-role"
  assume_role_policy = jsonencode({
    Version   = "2012-10-17",
    Statement = [{
      Action    = "sts:AssumeRole",
      Effect    = "Allow",
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

# Kinesis Stream 읽기, DynamoDB 쓰기, CloudWatch 로그 쓰기 권한을 포함하는 정책
resource "aws_iam_policy" "processor_lambda_policy" {
  name        = "ad-scouter-processor-lambda-policy"
  description = "Policy for the data processor Lambda"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = [
          "kinesis:GetRecords",
          "kinesis:GetShardIterator",
          "kinesis:DescribeStream",
          "kinesis:ListShards",
          "kinesis:ListStreams"
        ],
        Resource = var.kinesis_stream_arn # 데이터 소스
      },
      {
        Effect   = "Allow",
        Action   = [
          "dynamodb:PutItem",
          "dynamodb:UpdateItem"
        ],
        Resource = aws_dynamodb_table.stats_table.arn # 데이터 저장소
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

# 생성한 정책을 Lambda 실행 역할에 연결합니다.
resource "aws_iam_role_policy_attachment" "processor_policy_attachment" {
  role       = aws_iam_role.processor_lambda_role.name
  policy_arn = aws_iam_policy.processor_lambda_policy.arn
}


# --- Lambda Function ---
data "archive_file" "processor_zip" {
  type        = "zip"
  source_dir  = "${path.module}/src"
  output_path = "${path.module}/dist/processor.zip"
}

resource "aws_lambda_function" "processor_lambda" {
  function_name    = "ad-scouter-data-processor"
  handler          = "processor.handler"
  runtime          = "python3.11"
  role             = aws_iam_role.processor_lambda_role.arn
  
  filename         = data.archive_file.processor_zip.output_path
  source_code_hash = data.archive_file.processor_zip.output_base64sha256

  timeout = 300 # 5분 타임아웃

  environment {
    variables = {
      STATS_TABLE_NAME   = aws_dynamodb_table.stats_table.name
      # GEMINI_API_KEY = var.gemini_api_key # 추후 Gemini API 키를 여기에 추가
    }
  }
}

# --- Event Source Mapping ---
# Kinesis 스트림과 Lambda 함수를 연결합니다.
# 스트림에 데이터가 들어오면 이 Lambda를 자동으로 트리거합니다.
resource "aws_lambda_event_source_mapping" "kinesis_mapping" {
  event_source_arn  = var.kinesis_stream_arn
  function_name     = aws_lambda_function.processor_lambda.arn
  starting_position = "LATEST"
  batch_size        = 100 # 한 번에 최대 100개의 레코드를 가져와 처리
}

output "dynamodb_table_name" {
  value = aws_dynamodb_table.stats_table.name
}

output "dynamodb_stream_arn" {
  description = "The ARN of the DynamoDB stream."
  value       = aws_dynamodb_table.stats_table.stream_arn
}
