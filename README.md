# Ad-Scouter AI Analytics Platform

Ad-Scouter AI는 웹사이트 사용자 상호작용을 분석하고 AI 기반 인사이트를 제공하는 분석 플랫폼입니다.

## 프로젝트 구조

```
ad-scouter-ai/
├── packages/
│   └── sdk/                 # 웹용 분석 SDK
│       ├── src/
│       │   └── index.js     # SDK 핵심 코드
│       ├── dist/            # 빌드된 SDK 파일
│       ├── package.json     # SDK 패키지 설정
│       └── webpack.config.js # 빌드 설정
├── services/
│   ├── api-gateway/         # 데이터 수집 API 서버
│   │   ├── src/
│   │   │   └── ingest.py    # Lambda 함수 코드
│   │   ├── main.tf          # Terraform 인프라 설정
│   │   ├── variables.tf     # Terraform 변수
│   │   └── README.md        # API 서비스 문서
│   ├── data-processor/       # 데이터 처리 및 분석 서비스
│   │   ├── src/
│   │   │   └── processor.py # Kinesis 데이터 처리 Lambda
│   │   ├── main.tf          # DynamoDB 및 Lambda 설정
│   │   ├── variables.tf     # Terraform 변수
│   │   └── README.md        # 데이터 처리 서비스 문서
│   ├── scouter/             # 잠재 광고주 자동 발굴 서비스
│   │   ├── src/
│   │   │   └── scouter.py   # DynamoDB 스트림 처리 Lambda
│   │   ├── main.tf          # 스카우터 Lambda 설정
│   │   ├── variables.tf    # Terraform 변수
│   │   └── README.md        # 스카우터 서비스 문서
│   ├── ad-engine/           # AI 기반 광고 배출 및 매칭 엔진
│   │   ├── src/
│   │   │   ├── ad_generator.py # 광고 생성 Lambda
│   │   │   └── vectorizer.py  # 벡터화 Lambda
│   │   ├── main.tf          # RDS, Lambda, API Gateway 설정
│   │   ├── variables.tf     # Terraform 변수
│   │   └── README.md        # 광고 엔진 서비스 문서
│   └── platform/           # 고객용 웹 플랫폼 및 대시보드
│       ├── src/
│       │   ├── app/
│       │   │   ├── dashboard/ # 고객 대시보드
│       │   │   ├── login/     # 로그인 페이지
│       │   │   └── signup/    # 회원가입 페이지
│       │   └── components/
│       │       └── auth/     # 인증 컴포넌트
│       ├── main.tf          # Cognito 인증 설정
│       ├── variables.tf     # Terraform 변수
│       └── README.md        # 플랫폼 서비스 문서
├── docker-compose.yml       # 로컬 개발 환경 설정
├── package.json             # 루트 패키지 설정
├── .gitignore              # Git 제외 파일 목록
└── .github/
    └── workflows/          # GitHub Actions CI/CD 파이프라인
        ├── reusable-terraform-deploy.yml      # 재사용 가능한 Terraform 배포
        ├── security-enhanced-deploy.yml       # 보안 강화 배포 (수동 승인)
        ├── deploy-api-gateway.yml             # API Gateway 배포
        ├── deploy-data-processor.yml          # 데이터 프로세서 배포
        ├── deploy-scouter.yml                 # 스카우터 배포
        ├── deploy-ad-engine.yml               # 광고 엔진 배포
        ├── deploy-platform.yml                # 플랫폼 배포
        ├── build-and-deploy-sdk.yml           # SDK 빌드 및 배포
        ├── build-and-deploy-platform.yml      # 플랫폼 빌드 및 배포
        └── test-all-services.yml              # 전체 서비스 테스트
```

## SDK 사용법

### 1. SDK 설치

```html
<script>
  window.AD_SCOUTER_API_KEY = 'your-api-key-here';
</script>
<script src="https://cdn.your-domain.com/ad-scouter-sdk.js"></script>
```

### 2. SDK 초기화 및 사용

```javascript
// SDK 초기화
adScouter.init({
  // 초기화 옵션
});

// 이벤트 추적
adScouter.track('question_asked', {
  question: '사용자가 질문한 내용',
  category: 'product_inquiry'
});

adScouter.track('answer_received', {
  answer: 'AI가 제공한 답변',
  response_time: 1500
});
```

## 개발 환경 설정

### 1. 의존성 설치

```bash
npm install
```

### 2. SDK 빌드

```bash
npm run build:sdk
```

### 3. 로컬 개발 서버 실행

```bash
npm run dev
```

## 빌드 및 배포

### SDK 빌드

```bash
cd packages/sdk
npm install
npm run build
```

빌드된 파일은 `packages/sdk/dist/ad-scouter-sdk.js`에 생성됩니다.

### API Gateway 배포 (AWS)

```bash
cd services/api-gateway
terraform init
terraform plan
terraform apply
```

### Docker를 이용한 로컬 테스트

```bash
docker-compose up --build
```

- API Gateway: http://localhost:3000
- SDK 테스트 서버: http://localhost:8080

## 현재 구현 상태

### ✅ 완료된 기능
- [x] 웹용 분석 SDK 기본 구조 (v0.1)
- [x] AWS Lambda 데이터 수집 API
- [x] Terraform 인프라 코드
- [x] CORS 지원 및 보안 검증
- [x] Git 버전 관리 및 GitHub 연동
- [x] Amazon Kinesis 데이터 스트림 연동
- [x] 실시간 데이터 파이프라인 구축
- [x] 데이터 처리 및 분석 엔진 (DynamoDB 연동)
- [x] Gemini API 의도 분석 시스템 (Mock 구현)
- [x] 잠재 광고주 자동 발굴 시스템 (DynamoDB Stream 연동)
- [x] 완전한 End-to-End 파이프라인 구축
- [x] AI 기반 광고 배출 및 매칭 엔진 (RDS + pgvector)
- [x] 코사인 유사도 기반 광고 매칭 시스템
- [x] 실시간 맞춤형 광고 생성 API
- [x] 고객용 웹 플랫폼 및 대시보드 (Next.js)
- [x] AWS Cognito 기반 사용자 인증 시스템
- [x] 전문적인 기업 웹사이트 및 브랜딩
- [x] 완전 자동화된 CI/CD 파이프라인 (GitHub Actions)
- [x] 보안 강화된 배포 프로세스 (수동 승인)
- [x] 코드 품질 관리 및 자동 테스트
- [x] 프로덕션 수준의 운영 환경 구축

### 🚧 진행 중인 작업
- [ ] Gemini API 실제 연동
- [ ] 데이터 비식별화 처리 (Microsoft Presidio)
- [ ] 영업 자동화 (S3, SES 연동)
- [ ] 실시간 모니터링 대시보드
- [ ] 광고 성과 추적 시스템
- [ ] 고급 인증 기능 (MFA, 소셜 로그인)

## CI/CD 파이프라인

### 자동화된 배포 시스템
이 프로젝트는 GitHub Actions를 사용한 완전 자동화된 CI/CD 파이프라인을 갖추고 있습니다.

#### 배포 프로세스
```
Git Push → GitHub Actions → Code Scan → Terraform Plan → Manual Approval → Terraform Apply → Deployed to AWS
```

#### 주요 기능
- **자동 테스트**: 모든 서비스의 코드 품질 및 기능 테스트
- **보안 스캔**: CodeQL 및 Trivy를 통한 취약점 검사
- **수동 승인**: 프로덕션 배포 전 책임자 승인 필수
- **롤백 지원**: 문제 발생 시 즉시 이전 상태로 복구

#### 워크플로우 구성
- **재사용 가능한 워크플로우**: 모든 서비스에서 공통 사용
- **서비스별 배포**: 각 마이크로서비스 독립적 배포
- **환경별 분리**: 개발/스테이징/프로덕션 환경 분리

### 설정 방법
1. **GitHub Secrets 설정**: `.github/SECRETS_SETUP.md` 참조
2. **AWS 자격 증명**: IAM 사용자 및 권한 설정
3. **워크플로우 활성화**: main 브랜치 push 시 자동 실행

자세한 내용은 [CI/CD 문서](.github/CI_CD_DOCUMENTATION.md)를 참조하세요.

## 라이선스

MIT License

## 버전

현재 버전: 0.1.0

## 다음 단계

- [ ] API Gateway 서버 배포 및 테스트
- [ ] SDK 빌드 최적화
- [ ] 테스트 코드 작성
- [ ] CI/CD 파이프라인 구축
