# Ad-Scouter API Gateway Service

이 디렉토리는 Ad-Scouter AI의 데이터 수집 API Gateway 서비스를 포함합니다.

## 구조

```
api-gateway/
├── src/
│   └── ingest.py          # 데이터 수집 Lambda 함수
├── main.tf               # Terraform 메인 설정
├── variables.tf          # Terraform 변수 정의
├── package.json          # Node.js 패키지 설정
└── README.md            # 이 파일
```

## 배포 방법

### 1. 사전 요구사항

- AWS CLI 설치 및 구성
- Terraform 설치
- AWS 계정 접근 권한

### 2. AWS 자격 증명 설정

```bash
aws configure
```

### 3. Terraform 초기화 및 배포

```bash
# Terraform 초기화
terraform init

# 배포 계획 확인
terraform plan

# 인프라 배포
terraform apply
```

### 4. API 엔드포인트 확인

배포 완료 후 출력되는 `api_endpoint_url`을 사용하여 API를 테스트할 수 있습니다.

## API 사용법

### 엔드포인트

```
POST {api_endpoint_url}/ingest
```

### 요청 예시

```javascript
const response = await fetch('https://your-api-id.execute-api.ap-northeast-2.amazonaws.com/ingest', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    apiKey: 'your-api-key',
    eventName: 'question_asked',
    properties: {
      question: '사용자 질문',
      category: 'product_inquiry'
    },
    timestamp: new Date().toISOString(),
    url: window.location.href,
    userAgent: navigator.userAgent
  })
});
```

### 응답

- **성공 (202)**: `{"message": "Event received successfully."}`
- **오류 (400)**: `{"message": "Bad Request: eventName is missing."}`
- **오류 (401)**: `{"message": "Unauthorized: API Key is missing."}`

## 보안 고려사항

- 현재는 모든 도메인에서 CORS를 허용하고 있습니다. 프로덕션에서는 허용된 도메인으로 제한해야 합니다.
- API 키 검증 로직을 실제 데이터베이스와 연동하여 강화해야 합니다.
- Rate limiting을 추가하여 DDoS 공격을 방지해야 합니다.

## 다음 단계

- [ ] API 키 관리 시스템 구축
- [ ] Kinesis Stream 연동
- [ ] CloudWatch 모니터링 설정
- [ ] Rate limiting 구현
