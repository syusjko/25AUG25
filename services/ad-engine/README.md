# Ad-Scouter Advertisement Engine Service

이 디렉토리는 Ad-Scouter AI의 AI 기반 광고 배출 및 매칭 엔진을 포함합니다.

## 구조

```
ad-engine/
├── src/
│   ├── ad_generator.py     # 광고 생성 및 매칭 Lambda 함수
│   └── vectorizer.py      # 광고주 정보 벡터화 Lambda 함수
├── main.tf                # Terraform 메인 설정 (RDS, Lambda, API Gateway)
├── variables.tf           # Terraform 변수 정의
├── package.json           # Node.js 패키지 설정
└── README.md             # 이 파일
```

## 기능

### AI 기반 광고 매칭 파이프라인

```
사용자 질문 → 벡터화 → 코사인 유사도 계산 → 최적 광고주 선택 → 맞춤형 광고 생성
```

1. **사용자 질문 벡터화**: Gemini Embedding API로 질문을 벡터로 변환
2. **유사도 계산**: 코사인 유사도로 가장 관련성 높은 광고주 찾기
3. **광고 생성**: Gemini API로 맞춤형 광고 콘텐츠 생성
4. **실시간 응답**: API Gateway를 통해 즉시 광고 반환

### 데이터베이스 구조

#### PostgreSQL with pgvector Extension

```sql
-- 광고주 테이블
CREATE TABLE advertisers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    ad_template TEXT,
    embedding VECTOR(768),  -- pgvector 확장 사용
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 벡터 유사도 검색 인덱스
CREATE INDEX ON advertisers USING ivfflat (embedding vector_cosine_ops);
```

### 코사인 유사도 기반 매칭

- **벡터 차원**: 768차원 (Gemini Embedding 모델 기준)
- **유사도 계산**: 코사인 유사도로 관련성 측정
- **임계값**: 설정 가능한 최소 유사도 기준

## 배포 방법

### 1. 사전 요구사항

- AWS CLI 설치 및 구성
- Terraform 설치
- PostgreSQL 클라이언트 (pgvector 설정용)

### 2. 환경 변수 설정

`terraform.tfvars` 파일을 생성하고 데이터베이스 비밀번호를 설정합니다:

```hcl
db_password = "YourSecurePassword123!"
```

### 3. 배포

```bash
# Terraform 초기화
terraform init

# 배포 계획 확인
terraform plan

# 인프라 배포 (RDS 생성에 10-15분 소요)
terraform apply
```

### 4. pgvector 확장 활성화

RDS 인스턴스 생성 후 PostgreSQL 클라이언트로 연결하여 pgvector 확장을 활성화합니다:

```bash
# RDS 엔드포인트 확인
terraform output db_host

# PostgreSQL 클라이언트로 연결
psql -h <RDS_ENDPOINT> -U admaster -d adscouterdb

# pgvector 확장 활성화
CREATE EXTENSION IF NOT EXISTS vector;
```

## API 사용법

### 엔드포인트

```
POST {ad_engine_api_url}/ads
```

### 요청 예시

```javascript
const response = await fetch('https://your-api-id.execute-api.ap-northeast-2.amazonaws.com/ads', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    query: '마이크로소프트의 AI 서비스 가격이 궁금합니다'
  })
});

const adResult = await response.json();
console.log(adResult);
```

### 응답 예시

```json
{
  "advertiser": {
    "id": 1,
    "name": "Microsoft",
    "description": "Microsoft AI and cloud services for enterprise solutions"
  },
  "ad_content": "Microsoft의 AI 솔루션으로 비즈니스를 혁신하세요! 무료 체험 신청",
  "similarity_score": 0.85,
  "user_query": "마이크로소프트의 AI 서비스 가격이 궁금합니다"
}
```

## 테스트 방법

### 1. 광고주 데이터 추가

```sql
INSERT INTO advertisers (name, description, ad_template) VALUES 
('Microsoft', 'Microsoft AI and cloud services for enterprise solutions', 'Microsoft의 AI 솔루션으로 비즈니스를 혁신하세요! 무료 체험 신청'),
('Google', 'Google Cloud Platform and AI services for businesses', 'Google Cloud로 스케일링하세요! 지금 시작하면 크레딧 제공'),
('Amazon', 'Amazon Web Services cloud computing platform', 'AWS로 클라우드 여정을 시작하세요! 신규 고객 특별 혜택');
```

### 2. 벡터화 실행

```bash
# Lambda 함수 직접 호출하여 벡터화
aws lambda invoke --function-name ad-scouter-vectorizer --payload '{"advertiser_info":{"id":1,"description":"Microsoft AI and cloud services"}}' response.json
```

### 3. 광고 생성 테스트

```bash
curl -X POST https://your-api-url/ads \
  -H "Content-Type: application/json" \
  -d '{"query": "클라우드 서비스 추천해주세요"}'
```

## 향후 확장 계획

### Phase 3.1: Gemini API 실제 연동
- [ ] Google AI Studio API 키 설정
- [ ] 실제 벡터 임베딩 생성
- [ ] 맞춤형 광고 콘텐츠 생성

### Phase 3.2: 고도화
- [ ] 광고 성과 추적 시스템
- [ ] A/B 테스트 기능
- [ ] 실시간 광고 최적화

### Phase 3.3: 확장
- [ ] 다국어 지원
- [ ] 이미지 광고 생성
- [ ] 동영상 광고 생성

## 모니터링

- **CloudWatch Logs**: Lambda 함수 실행 로그
- **RDS Metrics**: 데이터베이스 성능 지표
- **API Gateway Metrics**: API 호출량 및 응답 시간
- **Custom Metrics**: 광고 매칭 정확도, 사용자 만족도 등
