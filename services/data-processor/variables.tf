variable "aws_region" {
  description = "The AWS region to deploy resources in."
  type        = string
  default     = "ap-northeast-2"
}

variable "kinesis_stream_arn" {
  description = "The ARN of the Kinesis data stream to process."
  type        = string
  # 이 값은 services/api-gateway의 Terraform output에서 가져와야 합니다.
  # terraform.tfvars 파일에 `kinesis_stream_arn = "arn:aws:kinesis:..."` 형태로 값을 넣어주세요.
}
