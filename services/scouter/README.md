# Ad-Scouter Lead Scouting Service

이 디렉토리는 Ad-Scouter AI의 잠재 광고주 자동 발굴 및 영업 준비 서비스를 포함합니다.

## 구조

```
scouter/
├── src/
│   └── scouter.py         # DynamoDB 스트림 처리 Lambda 함수
├── main.tf                # Terraform 메인 설정
├── variables.tf           # Terraform 변수 정의
├── package.json           # Node.js 패키지 설정
└── README.md             # 이 파일
```

## 기능

### 잠재 광고주 자동 발굴 파이프라인

```
DynamoDB Stream → Scouter Lambda → Gemini API → 영업 전략 생성
```

1. **DynamoDB Stream**: 분석된 데이터의 실시간 변경 감지
2. **Scouter Lambda**: 잠재 광고주 식별 및 영업 전략 생성
3. **Gemini API**: 회사 정보 검색 및 맞춤형 콘텐츠 생성
4. **영업 준비**: 이메일 템플릿, 랜딩페이지 컨셉 등 생성

### 발굴 조건

- **의도 분석**: '구매 고려' 의도가 높은 질문
- **회사 식별**: 질문에서 언급된 특정 회사/제품 추출
- **맞춤 전략**: 회사별 특성에 맞는 영업 접근법 생성

### 지원 회사 (현재 Mock 구현)

- Microsoft, Google, Apple, Amazon
- Samsung, Naver, Kakao
- 향후 Gemini API로 확장 가능

## 배포 방법

### 1. 사전 요구사항

- AWS CLI 설치 및 구성
- Terraform 설치
- Data Processor 서비스가 이미 배포되어 있어야 함

### 2. DynamoDB Stream ARN 확인

Data Processor 서비스에서 DynamoDB Stream ARN을 확인합니다:

```bash
cd ../data-processor
terraform output dynamodb_stream_arn
```

### 3. 환경 변수 설정

`terraform.tfvars` 파일을 생성하고 DynamoDB Stream ARN을 설정합니다:

```hcl
dynamodb_stream_arn = "arn:aws:dynamodb:ap-northeast-2:123456789012:table/ad-scouter-stats/stream/2024-01-01T00:00:00.000"
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

## 테스트 방법

### 1. 테스트 질문 전송

SDK를 통해 '구매 고려' 의도를 유발하는 질문을 전송:

```javascript
adScouter.track('question_asked', {
  question: '마이크로소프트의 새로운 AI 기능 가격은 얼마인가요?',
  category: 'product_inquiry'
});
```

### 2. 파이프라인 확인

1. **API Gateway**: 데이터 수집
2. **Kinesis**: 실시간 스트림 저장
3. **Processor Lambda**: 의도 분석 ('구매 고려')
4. **DynamoDB**: 분석 결과 저장
5. **DynamoDB Stream**: 변경사항 감지
6. **Scouter Lambda**: 잠재 광고주 식별 ('Microsoft')

## 향후 확장 계획

### Phase 2.1: Gemini API 실제 연동
- [ ] Google AI Studio API 키 설정
- [ ] 회사 정보 실시간 검색
- [ ] 맞춤형 영업 콘텐츠 생성

### Phase 2.2: 영업 자동화
- [ ] S3 버킷에 영업 자료 저장
- [ ] SES를 통한 영업팀 알림
- [ ] CRM 시스템 연동

### Phase 2.3: 고도화
- [ ] 경쟁사 분석
- [ ] 예산 규모 추정
- [ ] 접근 우선순위 결정

## 모니터링

- **CloudWatch Logs**: Lambda 함수 실행 로그
- **DynamoDB Stream Metrics**: 스트림 처리량
- **Custom Metrics**: 발굴된 잠재 광고주 수, 성공률 등
