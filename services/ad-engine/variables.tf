variable "aws_region" {
  description = "The AWS region to deploy resources in."
  type        = string
  default     = "ap-northeast-2"
}

variable "db_password" {
  description = "Password for the RDS database master user."
  type        = string
  sensitive   = true # Terraform이 출력에 암호를 표시하지 않도록 합니다.
  # terraform.tfvars 파일에 `db_password = "YourSecurePassword"` 형태로 값을 넣어주세요.
}
