# CI/CD 파이프라인 문서

Ad-Scouter AI 프로젝트의 완전 자동화된 CI/CD 파이프라인에 대한 상세 문서입니다.

## 아키텍처 개요

```
Git Push → GitHub Actions → Code Scan → Terraform Plan → Manual Approval → Terraform Apply → Deployed to AWS
```

## 워크플로우 구조

### 1. 재사용 가능한 워크플로우
- **`reusable-terraform-deploy.yml`**: 모든 서비스에서 공통으로 사용하는 Terraform 배포 로직
- **`security-enhanced-deploy.yml`**: 보안 강화된 배포 프로세스 (수동 승인 포함)

### 2. 서비스별 배포 워크플로우
- **`deploy-api-gateway.yml`**: API Gateway 서비스 배포
- **`deploy-data-processor.yml`**: 데이터 프로세서 서비스 배포
- **`deploy-scouter.yml`**: 스카우터 서비스 배포
- **`deploy-ad-engine.yml`**: 광고 엔진 서비스 배포
- **`deploy-platform.yml`**: 플랫폼 서비스 배포

### 3. 빌드 및 배포 워크플로우
- **`build-and-deploy-sdk.yml`**: SDK 빌드 및 CDN 배포
- **`build-and-deploy-platform.yml`**: 플랫폼 빌드 및 배포

### 4. 테스트 워크플로우
- **`test-all-services.yml`**: 전체 서비스 테스트 및 통합 테스트

## 배포 프로세스

### 자동 배포 트리거
- **브랜치**: `main` 브랜치에 push될 때 자동 실행
- **경로 필터링**: 각 서비스의 코드 변경 시에만 해당 워크플로우 실행
- **수동 실행**: `workflow_dispatch`를 통한 수동 배포 지원

### 보안 강화 배포 (프로덕션)
1. **코드 스캔**: CodeQL 및 Trivy를 통한 보안 취약점 검사
2. **Terraform Plan**: 변경사항 미리보기
3. **수동 승인**: 책임자의 승인 필수
4. **자동 배포**: 승인 후 자동으로 AWS에 배포

### 일반 배포 (개발/스테이징)
1. **Terraform Plan**: 변경사항 확인
2. **자동 배포**: main 브랜치 push 시 자동 배포

## 보안 기능

### 1. 정적 코드 분석
- **CodeQL**: GitHub의 정적 분석 도구로 보안 취약점 탐지
- **Trivy**: 컨테이너 및 파일 시스템 취약점 스캔
- **SARIF 업로드**: 결과를 GitHub Security 탭에 자동 업로드

### 2. 수동 승인 프로세스
- **Manual Approval**: 프로덕션 배포 전 필수 승인 단계
- **승인자 지정**: 특정 사용자만 승인 가능
- **이슈 생성**: 승인 요청을 GitHub 이슈로 자동 생성

### 3. 암호화된 Secrets
- **AWS 자격 증명**: 암호화된 GitHub Secrets 사용
- **서비스별 변수**: 각 서비스의 민감한 설정값 분리 관리

## 모니터링 및 알림

### 1. Slack 통합
- **배포 알림**: 성공/실패 상태를 Slack 채널로 전송
- **상세 정보**: 브랜치, 커밋, 작성자 정보 포함

### 2. GitHub Actions 대시보드
- **실행 상태**: 모든 워크플로우의 실행 상태 실시간 확인
- **로그 확인**: 각 단계별 상세 로그 제공
- **아티팩트**: 빌드 결과물 자동 저장

## 환경별 배포 전략

### 개발 환경
- **자동 배포**: 코드 push 시 즉시 배포
- **빠른 피드백**: 개발자가 즉시 변경사항 확인 가능

### 스테이징 환경
- **자동 배포**: main 브랜치 머지 시 배포
- **통합 테스트**: 전체 서비스 간 연동 테스트

### 프로덕션 환경
- **수동 승인**: 책임자의 명시적 승인 필수
- **보안 스캔**: 모든 보안 검사 통과 후 배포
- **롤백 준비**: 문제 발생 시 즉시 롤백 가능

## 롤백 전략

### 1. Terraform 롤백
```bash
# 이전 상태로 롤백
terraform plan -destroy
terraform apply -destroy
```

### 2. 코드 롤백
```bash
# 이전 커밋으로 되돌리기
git revert HEAD
git push origin main
```

### 3. 긴급 배포
- **워크플로우 수동 실행**: GitHub Actions에서 즉시 실행
- **핫픽스**: 긴급 수정사항을 별도 브랜치로 배포

## 성능 최적화

### 1. 병렬 실행
- **독립적 서비스**: 서로 의존성이 없는 서비스는 병렬 배포
- **캐시 활용**: npm, pip 캐시로 빌드 시간 단축

### 2. 조건부 실행
- **경로 필터링**: 변경된 서비스만 배포
- **스마트 트리거**: 불필요한 배포 방지

### 3. 아티팩트 관리
- **빌드 결과 저장**: 재사용 가능한 빌드 결과물 보관
- **자동 정리**: 오래된 아티팩트 자동 삭제

## 문제 해결

### 일반적인 문제
1. **권한 오류**: AWS IAM 권한 확인
2. **Terraform 오류**: 상태 파일 및 변수 확인
3. **빌드 실패**: 의존성 및 환경 설정 확인

### 디버깅 방법
1. **GitHub Actions 로그**: 각 단계별 상세 로그 확인
2. **AWS CloudWatch**: Lambda 함수 및 API Gateway 로그
3. **Terraform 상태**: `terraform show` 명령어로 현재 상태 확인

## 확장 계획

### 단기 계획
- [ ] 테스트 커버리지 향상
- [ ] 성능 테스트 자동화
- [ ] 데이터베이스 마이그레이션 자동화

### 장기 계획
- [ ] Blue-Green 배포 구현
- [ ] 카나리 배포 지원
- [ ] 다중 리전 배포

## 참고 자료
- [GitHub Actions 문서](https://docs.github.com/en/actions)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
