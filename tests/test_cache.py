import pytest
import json
from datetime import datetime, timedelta
from sqlitedict import SqliteDict
import diskcache
from schemas.cache_data import CacheData
import entity.user_entity as models
import schemas.user_schemas as schemas
import service.user_service as crud
from util.user_util import encode_jwt_token, get_user_by_jwt_token


def test_token_cache_storage(test_token_cache):
    """토큰 캐시 저장 및 조회 테스트"""
    # 테스트 데이터
    test_data = "[{\"id\": 1, \"value\": \"test\"}]"
    test_std_id = "12345678"
    
    # 현재 시간
    now = datetime.now()
    
    # 캐시 저장
    test_token_cache.set(
        f"attend_data_{test_std_id}",
        CacheData(data=test_data, updated_time=now),
        expire=60 * 60  # 1시간
    )
    
    # 캐시 조회
    cached_data = test_token_cache.get(f"attend_data_{test_std_id}")
    assert cached_data is not None
    assert cached_data.data == test_data
    assert cached_data.updated_time == now


def test_token_cache_expiration(test_token_cache):
    """토큰 캐시 만료 테스트"""
    # 테스트 데이터
    test_data = "[{\"id\": 1, \"value\": \"test\"}]"
    test_std_id = "12345678"
    
    # 캐시 저장 (1초 후 만료)
    test_token_cache.set(
        f"attend_data_{test_std_id}",
        CacheData(data=test_data, updated_time=datetime.now()),
        expire=1
    )
    
    # 캐시 확인
    cached_data = test_token_cache.get(f"attend_data_{test_std_id}")
    assert cached_data is not None
    
    # 2초 대기
    import time
    time.sleep(2)
    
    # 캐시 확인 (만료됨)
    expired_data = test_token_cache.get(f"attend_data_{test_std_id}")
    assert expired_data is None


def test_user_db_access(test_user_db):
    """SqliteDict 사용자 DB 접근 테스트"""
    # 테스트 데이터
    test_key = "test_key"
    test_value = {"data": "test_value", "timestamp": datetime.now().isoformat()}
    
    # DB에 저장
    test_user_db[test_key] = test_value
    test_user_db.commit()
    
    # DB에서 조회
    retrieved_value = test_user_db.get(test_key)
    assert retrieved_value is not None
    assert retrieved_value["data"] == test_value["data"]
    assert retrieved_value["timestamp"] == test_value["timestamp"]
    
    # 존재하지 않는 키 조회
    non_existent = test_user_db.get("non_existent_key")
    assert non_existent is None


def test_cache_with_token_login(client, test_db, test_token_cache):
    """토큰 로그인 및 캐시 사용 테스트"""
    # 테스트 사용자 생성
    test_user = schemas.UserCreate(
        username="12345678",
        password="test1234"
    )
    user = crud.create_user(db=test_db, user=test_user)
    
    # 테스트 데이터
    test_data = json.dumps([{"id": 1, "name": "Test Data"}])
    
    # 데이터 업데이트
    crud.update_user_by_username(
        test_db,
        username=user.username,
        user_update=schemas.UserUpdate(attend_data=test_data)
    )
    
    # 토큰 생성
    user = crud.get_user_by_username(test_db, username=user.username)
    token = encode_jwt_token(user)
    
    # 토큰으로 첫 로그인 (캐시에 저장)
    first_login_data = {
        "std_id": "12345678",
        "password": token,
        "type": 0,
        "account_register": False,
        "data": "",
        "force_new_data": False
    }
    
    response = client.post("/account/action", json=first_login_data)
    assert response.status_code == 200
    first_response = response.json()
    assert first_response["success"] is True
    assert first_response["data"] == test_data
    
    # 캐시 확인
    cached_data = test_token_cache.get(f"attend_data_12345678")
    assert cached_data is not None
    assert cached_data.data == test_data
    
    # 다시 데이터 변경 (DB만 변경, 캐시는 그대로)
    new_test_data = json.dumps([{"id": 2, "name": "Updated Data"}])
    crud.update_user_by_username(
        test_db,
        username=user.username,
        user_update=schemas.UserUpdate(attend_data=new_test_data)
    )
    
    # 토큰으로 두 번째 로그인 (캐시 사용)
    second_login_data = {
        "std_id": "12345678",
        "password": token,
        "type": 0,
        "account_register": False,
        "data": "",
        "force_new_data": False
    }
    
    response = client.post("/account/action", json=second_login_data)
    second_response = response.json()
    
    # 캐시된 데이터가 반환되므로 첫 번째 데이터와 같아야 함
    assert second_response["data"] == test_data
    
    # 캐시 무시 옵션 사용
    force_new_data = {
        "std_id": "12345678",
        "password": token,
        "type": 0,
        "account_register": False,
        "data": "",
        "force_new_data": True
    }
    
    response = client.post("/account/action", json=force_new_data)
    force_response = response.json()
    
    # 최신 DB 데이터가 반환되어야 함
    assert force_response["data"] == new_test_data
