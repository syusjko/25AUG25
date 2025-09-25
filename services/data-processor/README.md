# Ad-Scouter Data Processor Service

이 디렉토리는 Ad-Scouter AI의 데이터 처리 및 분석 서비스를 포함합니다.

## 구조

```
data-processor/
├── src/
│   └── processor.py        # Kinesis 데이터 처리 Lambda 함수
├── main.tf                # Terraform 메인 설정
├── variables.tf           # Terraform 변수 정의
├── package.json           # Node.js 패키지 설정
└── README.md             # 이 파일
```

## 기능

### 데이터 처리 파이프라인

```
Kinesis Stream → Lambda Processor → Gemini API → DynamoDB
```

1. **Kinesis Stream**: 실시간 데이터 수집
2. **Lambda Processor**: 데이터 디코딩 및 전처리
3. **Gemini API**: 텍스트 의도 분석 (현재 Mock 구현)
4. **DynamoDB**: 분석 결과 저장

### 분석 기능

- **의도 분석**: 사용자 질문의 의도를 분류
  - 정보 탐색
  - 구매 고려
  - 기능 문의
  - 단순 대화
  - 기타

- **비식별화**: 개인정보 마스킹 (향후 구현 예정)

## 배포 방법

### 1. 사전 요구사항

- AWS CLI 설치 및 구성
- Terraform 설치
- API Gateway 서비스가 이미 배포되어 있어야 함

### 2. Kinesis Stream ARN 확인

API Gateway 서비스에서 Kinesis Stream ARN을 확인합니다:

```bash
cd ../api-gateway
terraform output kinesis_stream_arn
```

### 3. 환경 변수 설정

`terraform.tfvars` 파일을 생성하고 Kinesis Stream ARN을 설정합니다:

```hcl
kinesis_stream_arn = "arn:aws:kinesis:ap-northeast-2:123456789012:stream/ad-scouter-ingest-stream"
```

### 4. 배포

```bash
# Terraform 초기화
terraform init

# 배포 계획 확인
terraform plan

# 인프라 배포
terraform apply
```

## DynamoDB 테이블 구조

### 테이블: `ad-scouter-stats`

| 필드 | 타입 | 설명 |
|------|------|------|
| customerId | String | 고객사 ID (API Key) |
| eventId | String | 이벤트 고유 ID |
| eventName | String | 이벤트 이름 |
| intent | String | 분석된 의도 |
| originalQuestion | String | 원본 질문 |
| timestamp | String | 이벤트 발생 시간 |

## Gemini API 연동

현재는 Mock 구현으로 되어 있습니다. 실제 Gemini API를 사용하려면:

1. Google AI Studio에서 API 키 발급
2. `processor.py`에서 주석 처리된 코드 활성화
3. Lambda Layer 또는 배포 패키지에 `google-generativeai` 라이브러리 포함

## 모니터링

- **CloudWatch Logs**: Lambda 함수 실행 로그
- **DynamoDB Metrics**: 테이블 사용량 및 성능 지표
- **Kinesis Metrics**: 스트림 처리량 및 지연 시간

## 다음 단계

- [ ] Gemini API 실제 연동
- [ ] Microsoft Presidio를 활용한 비식별화 구현
- [ ] 실시간 대시보드 구축
- [ ] 알림 시스템 구현
