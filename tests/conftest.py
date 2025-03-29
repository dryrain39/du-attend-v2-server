import pytest
import os
import sys
import tempfile
import shutil
from sqlitedict import SqliteDict
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import diskcache
from unittest.mock import patch, MagicMock

# 테스트 환경 설정
os.environ["TESTING"] = "1"

# 프로젝트 루트 경로를 추가하여 import가 제대로 동작하도록 설정
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 실제 DB 연결을 방지하기 위한 패치
from database.db import Base, get_session

# FastAPI 앱 import 전에 패치 설정
original_engine = None
with patch('sqlalchemy.create_engine') as mock_create_engine:
    # Mock 엔진 반환
    mock_engine = MagicMock()
    mock_create_engine.return_value = mock_engine

    # main 앱 import
    from main import app
    from config.config import USER_DB_PATH


# SQLAlchemy 테스트 DB 설정
@pytest.fixture(scope="function")
def test_db():
    # 임시 DB 파일 생성
    tmp_db_file = tempfile.NamedTemporaryFile(delete=False)
    tmp_db_file.close()

    # 테스트용 SQLite 엔진 생성
    test_engine = create_engine(f"sqlite:///{tmp_db_file.name}", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

    # DB 스키마 생성
    # SQLAlchemy 2.0에서는 connect()에 트랜잭션 컨텍스트 사용
    with test_engine.begin() as conn:
        # Users 테이블만 생성 시도
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER NOT NULL PRIMARY KEY, 
            username VARCHAR UNIQUE, 
            password VARCHAR, 
            updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, 
            attend_data TEXT
        )
        """))

        # 인덱스 생성
        conn.execute(text("CREATE INDEX IF NOT EXISTS ix_users_id ON users (id)"))
        conn.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS ix_users_username ON users (username)"))

        # 테스트에 필요한 다른 테이블도 필요하면 여기에 추가
        # begin() 컨텍스트를 사용하면 자동으로 commit됨

    # 세션 오버라이드 함수
    def override_get_session():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    # FastAPI 의존성 오버라이드
    app.dependency_overrides[get_session] = override_get_session

    # 테스트용 세션 제공
    db = TestingSessionLocal()
    yield db

    # 테스트 후 정리
    db.close()
    # os.unlink(tmp_db_file.name)


# SqliteDict 테스트 설정
@pytest.fixture(scope="function")
def test_user_db():
    # 임시 디렉토리 생성
    temp_dir = tempfile.mkdtemp()
    test_db_path = os.path.join(temp_dir, "test_database.sqlite")

    # 테스트용 SqliteDict 생성
    user_db = SqliteDict(test_db_path, autocommit=False)

    # 테스트에 DB 제공
    yield user_db

    # 테스트 후 정리
    user_db.close()
    # shutil.rmtree(temp_dir)


# 토큰 캐시 테스트 설정
@pytest.fixture(scope="function")
def test_token_cache():
    # 임시 디렉토리 생성
    temp_dir = tempfile.mkdtemp()

    # 테스트용 DiskCache 생성
    token_cache = diskcache.FanoutCache(temp_dir)

    # 테스트에 캐시 제공
    yield token_cache

    # 테스트 후 정리
    token_cache.close()
    # shutil.rmtree(temp_dir)


# API 테스트 클라이언트
@pytest.fixture(scope="function")
def client(test_db, test_user_db, test_token_cache):
    # 원본 경로 백업
    original_user_db_path = USER_DB_PATH

    # SqliteDict 및 DiskCache 패치를 위한 import
    import service.login
    import route.user.account_v2

    # 원본 객체 백업
    original_login_user_db = service.login.USER_DB
    original_login_token_cache = service.login.TOKEN_CACHE
    original_account_user_db = route.user.account_v2.USER_DB
    original_account_token_cache = route.user.account_v2.TOKEN_CACHE

    # 테스트 객체로 교체
    service.login.USER_DB = test_user_db
    service.login.TOKEN_CACHE = test_token_cache
    route.user.account_v2.USER_DB = test_user_db
    route.user.account_v2.TOKEN_CACHE = test_token_cache

    # 테스트 클라이언트 생성
    with TestClient(app) as client:
        yield client

    # 원래 객체로 복원
    service.login.USER_DB = original_login_user_db
    service.login.TOKEN_CACHE = original_login_token_cache
    route.user.account_v2.USER_DB = original_account_user_db
    route.user.account_v2.TOKEN_CACHE = original_account_token_cache
