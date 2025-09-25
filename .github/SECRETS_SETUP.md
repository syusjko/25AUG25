# GitHub Secrets 설정 가이드

이 문서는 Ad-Scouter AI 프로젝트의 CI/CD 파이프라인을 위한 GitHub Secrets 설정 방법을 안내합니다.

## 필수 Secrets

### AWS 자격 증명
- `AWS_ACCESS_KEY_ID`: AWS IAM 사용자의 액세스 키 ID
- `AWS_SECRET_ACCESS_KEY`: 해당 액세스 키의 시크릿 키

### 서비스별 Terraform 변수
- `DATA_PROCESSOR_TF_VARS`: 데이터 프로세서 서비스용 Terraform 변수
- `SCOUTER_TF_VARS`: 스카우터 서비스용 Terraform 변수
- `AD_ENGINE_TF_VARS`: 광고 엔진 서비스용 Terraform 변수

### 배포 관련
- `CLOUDFRONT_DISTRIBUTION_ID`: CloudFront 배포 ID (SDK CDN용)
- `SLACK_WEBHOOK_URL`: Slack 알림용 웹훅 URL (선택사항)

## 설정 방법

### 1. GitHub 저장소 접속
1. 프로젝트의 GitHub 저장소로 이동
2. `Settings` 탭 클릭
3. 왼쪽 메뉴에서 `Secrets and variables` > `Actions` 선택

### 2. AWS 자격 증명 설정

#### AWS IAM 사용자 생성
```bash
# AWS CLI로 IAM 사용자 생성
aws iam create-user --user-name ad-scouter-ci-cd

# 액세스 키 생성
aws iam create-access-key --user-name ad-scouter-ci-cd
```

#### 필요한 권한 정책
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "lambda:*",
                "apigateway:*",
                "dynamodb:*",
                "kinesis:*",
                "rds:*",
                "cognito:*",
                "s3:*",
                "cloudfront:*",
                "iam:*",
                "logs:*"
            ],
            "Resource": "*"
        }
    ]
}
```

### 3. GitHub Secrets 추가

#### AWS 자격 증명
- `AWS_ACCESS_KEY_ID`: 위에서 생성한 액세스 키 ID
- `AWS_SECRET_ACCESS_KEY`: 위에서 생성한 시크릿 액세스 키

#### 서비스별 Terraform 변수 예시

**DATA_PROCESSOR_TF_VARS:**
```hcl
aws_region = "ap-northeast-2"
kinesis_stream_arn = "arn:aws:kinesis:ap-northeast-2:123456789012:stream/ad-scouter-ingest-stream"
```

**SCOUTER_TF_VARS:**
```hcl
aws_region = "ap-northeast-2"
dynamodb_stream_arn = "arn:aws:dynamodb:ap-northeast-2:123456789012:table/ad-scouter-stats/stream/2024-01-01T00:00:00.000"
```

**AD_ENGINE_TF_VARS:**
```hcl
aws_region = "ap-northeast-2"
db_password = "your-secure-database-password"
```

### 4. 선택적 Secrets

#### Slack 알림 (선택사항)
- `SLACK_WEBHOOK_URL`: Slack 웹훅 URL
  - Slack 앱 생성 후 Incoming Webhooks 활성화
  - 웹훅 URL 복사하여 GitHub Secret에 추가

#### CloudFront 배포 ID (SDK CDN용)
- `CLOUDFRONT_DISTRIBUTION_ID`: CloudFront 배포 ID
  - AWS Console에서 CloudFront 배포 생성 후 ID 복사

## 보안 모범 사례

### 1. 최소 권한 원칙
- CI/CD용 IAM 사용자는 필요한 최소한의 권한만 부여
- 각 서비스별로 별도의 IAM 역할 사용 권장

### 2. 정기적 키 로테이션
```bash
# 액세스 키 로테이션 스크립트 예시
aws iam create-access-key --user-name ad-scouter-ci-cd
# 새 키를 GitHub Secrets에 업데이트
aws iam delete-access-key --user-name ad-scouter-ci-cd --access-key-id OLD_KEY_ID
```

### 3. 환경별 분리
- 개발/스테이징/프로덕션 환경별로 별도의 AWS 계정 사용 권장
- 각 환경별로 별도의 GitHub Secrets 설정

## 문제 해결

### 일반적인 오류
1. **AWS 자격 증명 오류**: IAM 사용자 권한 확인
2. **Terraform 변수 오류**: TF_VARS 형식 확인
3. **배포 실패**: AWS 리소스 한도 확인

### 로그 확인
- GitHub Actions 탭에서 워크플로우 실행 로그 확인
- AWS CloudWatch에서 Lambda 함수 로그 확인

## 참고 자료
- [GitHub Secrets 문서](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [AWS IAM 사용자 가이드](https://docs.aws.amazon.com/IAM/latest/UserGuide/)
- [Terraform AWS Provider 문서](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
