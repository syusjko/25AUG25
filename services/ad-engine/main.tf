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

# --- VPC & Networking (for RDS) ---
# RDS는 VPC 내에서 실행되어야 하므로, 기본 VPC와 서브넷을 사용합니다.
data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

resource "aws_db_subnet_group" "ad_db_subnet_group" {
  name       = "ad-scouter-db-subnet-group"
  subnet_ids = data.aws_subnets.default.ids
}

resource "aws_security_group" "rds_sg" {
  name        = "ad-scouter-rds-sg"
  description = "Allow PostgreSQL traffic"
  vpc_id      = data.aws_vpc.default.id

  # Lambda에서 접근할 수 있도록 인바운드 규칙을 설정합니다. (추후 Lambda SG ID로 제한)
  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # 프로덕션에서는 Lambda의 Security Group ID로 제한해야 합니다.
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# --- RDS PostgreSQL Instance with pgvector ---
# 광고주 정보와 벡터를 저장할 데이터베이스
resource "aws_db_instance" "ad_db" {
  identifier           = "ad-scouter-db-instance"
  allocated_storage    = 20
  engine               = "postgres"
  engine_version       = "15.3"
  instance_class       = "db.t3.micro" # 비용 최소화를 위해 Free Tier 사용
  db_name              = "adscouterdb"
  username             = "admaster"
  password             = var.db_password # 변수를 통해 안전하게 관리
  db_subnet_group_name = aws_db_subnet_group.ad_db_subnet_group.name
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  skip_final_snapshot  = true
  publicly_accessible  = true # Lambda에서 쉽게 접근하기 위해 임시로 허용. 프로덕션에서는 false로 변경
}

# --- IAM Role & Policy for Ad Engine Lambda ---
resource "aws_iam_role" "ad_engine_lambda_role" {
  name = "ad-scouter-ad-engine-lambda-role"
  assume_role_policy = jsonencode({
    Version   = "2012-10-17",
    Statement = [{
      Action    = "sts:AssumeRole",
      Effect    = "Allow",
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

# RDS 접근, CloudWatch 로그 쓰기 권한 정책
resource "aws_iam_policy" "ad_engine_lambda_policy" {
  name = "ad-scouter-ad-engine-lambda-policy"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
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

resource "aws_iam_role_policy_attachment" "ad_engine_policy_attachment" {
  role       = aws_iam_role.ad_engine_lambda_role.name
  policy_arn = aws_iam_policy.ad_engine_lambda_policy.arn
}

# --- Lambda Function for Vectorization ---
data "archive_file" "vectorizer_zip" {
  type        = "zip"
  source_dir  = "${path.module}/src"
  output_path = "${path.module}/dist/vectorizer.zip"
}

resource "aws_lambda_function" "vectorizer_lambda" {
  function_name    = "ad-scouter-vectorizer"
  handler          = "vectorizer.handler"
  runtime          = "python3.11"
  role             = aws_iam_role.ad_engine_lambda_role.arn
  
  filename         = data.archive_file.vectorizer_zip.output_path
  source_code_hash = data.archive_file.vectorizer_zip.output_base64sha256
  timeout          = 300 # 5분
  
  environment {
    variables = {
      DB_HOST       = aws_db_instance.ad_db.address
      DB_NAME       = aws_db_instance.ad_db.db_name
      DB_USER       = aws_db_instance.ad_db.username
      DB_PASSWORD   = var.db_password
      GEMINI_API_KEY = var.gemini_api_key
    }
  }
}

# --- Lambda Function for Ad Generation ---
data "archive_file" "ad_generator_zip" {
  type        = "zip"
  source_dir  = "${path.module}/src"
  output_path = "${path.module}/dist/ad_generator.zip"
}

resource "aws_lambda_function" "ad_generator_lambda" {
  function_name    = "ad-scouter-ad-generator"
  handler          = "ad_generator.handler"
  runtime          = "python3.11"
  role             = aws_iam_role.ad_engine_lambda_role.arn
  
  filename         = data.archive_file.ad_generator_zip.output_path
  source_code_hash = data.archive_file.ad_generator_zip.output_base64sha256
  timeout          = 300 # 5분
  
  environment {
    variables = {
      DB_HOST       = aws_db_instance.ad_db.address
      DB_NAME       = aws_db_instance.ad_db.db_name
      DB_USER       = aws_db_instance.ad_db.username
      DB_PASSWORD   = var.db_password
      GEMINI_API_KEY = var.gemini_api_key
    }
  }
}

# --- API Gateway for Ad Engine ---
resource "aws_apigatewayv2_api" "ad_engine_api" {
  name          = "ad-scouter-ad-engine-api"
  protocol_type = "HTTP"
  
  cors_configuration {
    allow_origins = ["*"]
    allow_methods = ["POST", "OPTIONS"]
    allow_headers = ["Content-Type"]
  }
}

resource "aws_apigatewayv2_integration" "ad_generator_integration" {
  api_id           = aws_apigatewayv2_api.ad_engine_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.ad_generator_lambda.invoke_arn
}

resource "aws_apigatewayv2_route" "ads_route" {
  api_id    = aws_apigatewayv2_api.ad_engine_api.id
  route_key = "POST /ads"
  target    = "integrations/${aws_apigatewayv2_integration.ad_generator_integration.id}"
}

resource "aws_apigatewayv2_stage" "ad_engine_stage" {
  api_id      = aws_apigatewayv2_api.ad_engine_api.id
  name        = "$default"
  auto_deploy = true
}

resource "aws_lambda_permission" "ad_engine_api_gw_permission" {
  statement_id  = "AllowAdEngineAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ad_generator_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.ad_engine_api.execution_arn}/*/*"
}

output "db_host" {
  value = aws_db_instance.ad_db.address
}
output "db_name" {
  value = aws_db_instance.ad_db.db_name
}
output "db_username" {
  value = aws_db_instance.ad_db.username
}
output "ad_engine_api_url" {
  description = "The URL for the Ad Engine API Gateway."
  value       = "${aws_apigatewayv2_api.ad_engine_api.api_endpoint}/ads"
}
