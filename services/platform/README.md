# Ad-Scouter AI Platform

이 디렉토리는 Ad-Scouter AI의 고객용 웹 플랫폼과 대시보드를 포함합니다.

## 구조

```
platform/
├── src/
│   ├── app/
│   │   ├── dashboard/        # 고객 대시보드 페이지
│   │   ├── login/           # 로그인 페이지
│   │   ├── signup/          # 회원가입 페이지
│   │   └── page.tsx         # 홈페이지
│   └── components/
│       └── auth/            # 인증 관련 컴포넌트
├── main.tf                  # Terraform 메인 설정 (Cognito)
├── variables.tf             # Terraform 변수 정의
├── package.json             # Next.js 패키지 설정
└── README.md               # 이 파일
```

## 기능

### 고객 플랫폼

- **홈페이지**: 서비스 소개 및 가치 제안
- **회원가입/로그인**: AWS Cognito 기반 안전한 인증
- **대시보드**: 실시간 데이터 분석 및 성과 모니터링
- **SDK 통합 가이드**: 웹사이트 연동 방법 안내

### 보안 기능

- **AWS Cognito**: 엔터프라이즈급 사용자 인증
- **비밀번호 정책**: 강력한 보안 요구사항
- **이메일 인증**: 자동 이메일 검증
- **세션 관리**: 안전한 로그인 상태 유지

## 개발 환경 설정

### 1. 사전 요구사항

- Node.js 18+ 설치
- AWS CLI 설치 및 구성
- Terraform 설치

### 2. 의존성 설치

```bash
npm install
```

### 3. 개발 서버 실행

```bash
npm run dev
```

개발 서버는 http://localhost:3000에서 실행됩니다.

### 4. AWS Cognito 배포

```bash
# Terraform 초기화
terraform init

# 배포 계획 확인
terraform plan

# Cognito 사용자 풀 생성
terraform apply
```

## 페이지 구조

### 홈페이지 (/)
- 서비스 소개 및 주요 기능 설명
- 회원가입/로그인 링크
- 작동 원리 및 혜택 안내

### 로그인 페이지 (/login)
- 이메일/비밀번호 로그인
- 데모 계정 정보 제공
- 회원가입 페이지 링크

### 회원가입 페이지 (/signup)
- 회사명, 이메일, 비밀번호 입력
- 비밀번호 정책 안내
- 무료 체험 혜택 설명

### 대시보드 (/dashboard)
- 총 호출 비용 현황
- 사용자 의도 분포 차트
- 발굴된 잠재 광고주 수
- 최근 활동 로그
- SDK 통합 가이드

## 인증 시스템

### AWS Cognito 설정

- **사용자 풀**: `ad-scouter-user-pool`
- **클라이언트**: `ad-scouter-dashboard-client`
- **인증 방식**: 이메일/비밀번호
- **비밀번호 정책**: 최소 8자, 대소문자, 숫자, 특수문자 필수

### 보안 기능

- **자동 이메일 검증**: 가입 시 이메일 인증 필수
- **세션 관리**: 안전한 로그인 상태 유지
- **OAuth 지원**: 향후 소셜 로그인 확장 가능

## 스타일링

### Tailwind CSS
- 반응형 디자인
- 일관된 디자인 시스템
- 다크/라이트 모드 지원 준비

### 컴포넌트 구조
- 재사용 가능한 UI 컴포넌트
- 타입 안전성을 위한 TypeScript
- 접근성 고려한 마크업

## 배포

### 개발 환경
```bash
npm run dev
```

### 프로덕션 빌드
```bash
npm run build
npm run start
```

### AWS 배포
```bash
# Cognito 인프라 배포
terraform apply

# 애플리케이션 배포 (Vercel, AWS Amplify 등)
npm run build
```

## 향후 확장 계획

### Phase 4.1: 고급 인증
- [ ] 소셜 로그인 (Google, Microsoft)
- [ ] 다단계 인증 (MFA)
- [ ] 역할 기반 접근 제어 (RBAC)

### Phase 4.2: 대시보드 고도화
- [ ] 실시간 데이터 시각화
- [ ] 커스터마이징 가능한 위젯
- [ ] 알림 및 알림 설정

### Phase 4.3: 고객 지원
- [ ] 실시간 채팅 지원
- [ ] FAQ 및 도움말 섹션
- [ ] API 문서 통합

## 모니터링

- **Next.js Analytics**: 페이지 뷰 및 성능 지표
- **AWS CloudWatch**: Cognito 사용자 활동 로그
- **Custom Metrics**: 사용자 행동 분석