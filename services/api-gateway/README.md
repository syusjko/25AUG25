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

## 데이터 파이프라인

### 현재 아키텍처

```
웹사이트 → SDK → API Gateway → Lambda → Kinesis Stream
```

1. **웹사이트**: 사용자 상호작용 데이터 생성
2. **SDK**: 데이터를 API Gateway로 전송
3. **API Gateway**: HTTP 요청을 Lambda로 라우팅
4. **Lambda**: 데이터 검증 후 Kinesis로 전송
5. **Kinesis Stream**: 실시간 데이터 스트림 저장

### Kinesis Stream 설정

- **스트림 이름**: `ad-scouter-ingest-stream`
- **샤드 수**: 1개 (초기 설정, 트래픽에 따라 조정 가능)
- **파티션 키**: API Key (동일 고객사 데이터는 동일 샤드로 분산)

## 다음 단계

- [x] Kinesis Stream 연동 완료
- [ ] 데이터 비식별화 처리 Lambda 구축
- [ ] CloudWatch 모니터링 설정
- [ ] Rate limiting 구현
