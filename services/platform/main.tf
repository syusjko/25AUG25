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

# --- Amazon Cognito User Pool ---
# 고객사 사용자의 계정을 관리할 사용자 풀을 생성합니다.
resource "aws_cognito_user_pool" "user_pool" {
  name = "ad-scouter-user-pool"
  
  # 사용자가 이메일로 가입하고 로그인하도록 설정
  schema {
    name                = "email"
    attribute_data_type = "String"
    required            = true
    mutable             = true
  }

  password_policy {
    minimum_length    = 8
    require_lowercase = true
    require_numbers   = true
    require_symbols   = true
    require_uppercase = true
  }

  auto_verified_attributes = ["email"]
}

# --- Cognito User Pool Client ---
# 웹 애플리케이션(대시보드)이 사용자 풀과 상호작용할 수 있도록 클라이언트를 생성합니다.
resource "aws_cognito_user_pool_client" "user_pool_client" {
  name         = "ad-scouter-dashboard-client"
  user_pool_id = aws_cognito_user_pool.user_pool.id

  # 클라이언트 시크릿을 생성하지 않음 (공개 클라이언트)
  generate_secret = false
  
  # 허용할 OAuth 흐름 및 스코프
  allowed_oauth_flows_user_pool_client = true
  allowed_oauth_flows                  = ["code", "implicit"]
  allowed_oauth_scopes                 = ["email", "openid", "profile"]
  
  # 로그인 및 로그아웃 후 리디렉션될 URL
  callback_urls        = ["http://localhost:3000/callback"] # 프로덕션에서는 실제 도메인으로 변경
  logout_urls          = ["http://localhost:3000/login"]
  supported_identity_providers = ["COGNITO"]
}

# --- 출력 ---
output "cognito_user_pool_id" {
  description = "The ID of the Cognito User Pool."
  value       = aws_cognito_user_pool.user_pool.id
}

output "cognito_user_pool_client_id" {
  description = "The ID of the Cognito User Pool Client."
  value       = aws_cognito_user_pool_client.user_pool_client.id
}
