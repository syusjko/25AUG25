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
│   └── api-gateway/         # 데이터 수집 API 서버
├── docker-compose.yml       # 로컬 개발 환경 설정
├── package.json             # 루트 패키지 설정
└── .gitignore              # Git 제외 파일 목록
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

### Docker를 이용한 로컬 테스트

```bash
docker-compose up --build
```

- API Gateway: http://localhost:3000
- SDK 테스트 서버: http://localhost:8080

## 라이선스

MIT License

## 버전

현재 버전: 0.1.0

## 다음 단계

- [ ] API Gateway 서버 구현
- [ ] SDK 빌드 최적화
- [ ] 테스트 코드 작성
- [ ] CI/CD 파이프라인 구축
