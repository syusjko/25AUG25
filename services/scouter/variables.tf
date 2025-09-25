variable "aws_region" {
  description = "The AWS region to deploy resources in."
  type        = string
  default     = "ap-northeast-2"
}

variable "dynamodb_stream_arn" {
  description = "The ARN of the DynamoDB stream to process."
  type        = string
  # 이 값은 services/data-processor의 Terraform output에서 가져와야 합니다.
  # terraform.tfvars 파일에 `dynamodb_stream_arn = "arn:aws:dynamodb:..."` 형태로 값을 넣어주세요.
}
