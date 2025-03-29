# 테스트 환경 구성 기록

## pytest 설정
- `pytest.ini` 파일 생성하여 테스트 경로 및 패턴 지정
- 프로젝트 루트 디렉토리를 Python 경로에 추가
- 환경 변수를 통한 테스트 모드 설정

## 테스트 픽스처
1. `test_db`: 테스트용 SQLite 데이터베이스 설정
2. `test_user_db`: 테스트용 SqliteDict 설정
3. `test_token_cache`: 테스트용 DiskCache 설정
4. `client`: FastAPI 테스트 클라이언트 설정

## 실제 DB 연결 방지
- 환경 변수로 테스트 모드 확인: `os.environ["TESTING"] = "1"`
- `sqlalchemy.create_engine` 패치하여 실제 DB 연결 방지
- FastAPI 애플리케이션 시작 시 테스트 모드에서는 DB 초기화 건너뛰기

## 테스트 실행 스크립트
- `run_tests.py`: Python 스크립트로 테스트 실행
- `run_tests.sh`: Shell 스크립트로 테스트 실행

## 주의사항
- 테스트 환경과 프로덕션 환경의 차이를 명확히 인지하고 설계
- 테스트 데이터베이스 스키마는 SQLite 호환성 고려 필요
- 테스트 후 리소스 정리 과정에서 Windows 환경 특유의 문제 발생 가능
