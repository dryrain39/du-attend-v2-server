# SqliteDict 제거 계획 작업 기록

## 목표
현재 프로젝트에서 SqliteDict 라이브러리를 제거하고 SQLAlchemy로 모든 데이터 접근을 통합하는 작업

## 작업 분석 내용

### 1. 현황 분석
- SqliteDict는 주로 USER_DB 변수를 통해 `./user_db/database.sqlite` 파일에 접근하는 데 사용됨
- 주로 로그인, 계정 관리 등의 기능에서 사용 중
- diskcache 라이브러리도 함께 사용하고 있음 (TOKEN_CACHE)
- SQLAlchemy와 FastAPI Users도 함께 사용되고 있음

### 2. 테스트 코드 작성
- 테스트 디렉토리 구조 생성 및 설정
- conftest.py에 SQLite 테스트 DB, SqliteDict 테스트 DB, 토큰 캐시 테스트 설정 구현
- 다음 테스트 파일 작성:
  - test_account.py: 계정 관련 기능 테스트
  - test_login_service.py: 로그인 서비스 단위 테스트
  - test_cache.py: 캐시 기능 테스트
  - test_migration.py: DB 마이그레이션 테스트

### 3. 발견된 문제점 및 해결
- SQLite에서 `ON UPDATE CURRENT_TIMESTAMP` 구문 지원 안함 -> SQLAlchemy의 `onupdate` 기능 사용
- SQLAlchemy Connection 객체의 commit 메소드 지원 안함 -> `with engine.begin()` 사용
- 테스트 URL 경로 불일치 -> API 경로를 맞게 수정 (/v2/user/account/action -> /account/action)
- DiskCache 라이브러리의 Windows 환경 파일 잠금 문제 -> 임시 파일 정리 시 예외 처리 필요

### 4. 완료된 작업
- User 및 Log 엔티티 모델 수정하여 SQLite 호환성 확보
- 테스트 환경에서 실제 CockroachDB 연결 방지
- 테스트 실행 환경 구성 (pytest.ini, conftest.py 등)
- 테스트 URL 경로 수정

### 5. 남은 작업
- DiskCache 파일 정리 문제 해결
- SqliteDict를 SQLAlchemy로 대체하는 실제 코드 작성
- 전체 테스트 실행 및 검증
- 데이터 마이그레이션 실행

## 고려해볼 솔루션
Windows 환경에서 DiskCache 파일 잠금 문제를 해결하기 위한 접근법:
1. `try-except` 블록으로 임시 파일 삭제 오류 처리
2. 짧은 지연 시간 및 gc.collect() 추가
3. 테스트 종료 후 일괄 정리
4. 파일 삭제 재시도 로직 구현
5. send2trash 패키지 사용
