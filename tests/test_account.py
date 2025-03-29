import pytest
import json
from datetime import datetime
import entity.user_entity as models
import schemas.user_schemas as schemas
import service.user_service as crud
from VO.account_vo import AccountAction, ChangePasswordAction
from schemas.cache_data import CacheData


def test_register_account(client, test_db):
    """회원가입 기능 테스트"""
    # 테스트 데이터 준비
    test_user = {
        "std_id": "12345678",
        "password": "test1234",
        "type": 0,
        "account_register": True,
        "data": ""
    }
    
    # API 호출
    response = client.post("/account/action", json=test_user)
    assert response.status_code == 200
    
    # 응답 검증
    data = response.json()
    assert data["success"] is True
    assert "new_token" in data
    
    # DB에 사용자가 생성되었는지 확인
    db_user = crud.get_user_by_username(test_db, username=test_user["std_id"])
    assert db_user is not None
    assert db_user.username == test_user["std_id"]


def test_login_with_password(client, test_db):
    """비밀번호를 사용한 로그인 테스트"""
    # 테스트 사용자 생성
    test_user = schemas.UserCreate(
        username="12345678",
        password="test1234"
    )
    user = crud.create_user(db=test_db, user=test_user)
    
    # 로그인 데이터 준비
    login_data = {
        "std_id": "12345678",
        "password": "test1234",
        "type": 0,
        "account_register": False,
        "data": "",
        "force_new_data": False
    }
    
    # API 호출
    response = client.post("/account/action", json=login_data)
    assert response.status_code == 200
    
    # 응답 검증
    data = response.json()
    assert data["success"] is True
    assert "new_token" in data
    assert "data" in data


def test_invalid_login(client, test_db):
    """잘못된 비밀번호로 로그인 실패 테스트"""
    # 테스트 사용자 생성
    test_user = schemas.UserCreate(
        username="12345678",
        password="test1234"
    )
    user = crud.create_user(db=test_db, user=test_user)
    
    # 잘못된 비밀번호로 로그인 시도
    login_data = {
        "std_id": "12345678",
        "password": "wrong_password",
        "type": 0,
        "account_register": False,
        "data": ""
    }
    
    # API 호출
    response = client.post("/account/action", json=login_data)
    assert response.status_code == 200
    
    # 응답 검증
    data = response.json()
    assert data["success"] is False
    assert data["code"] == "PWDIDNOTMATCH"


def test_login_with_token(client, test_db, test_token_cache):
    """토큰을 사용한 로그인 테스트"""
    # 테스트 사용자 생성
    test_user = schemas.UserCreate(
        username="12345678",
        password="test1234"
    )
    user = crud.create_user(db=test_db, user=test_user)
    
    # 먼저 비밀번호로 로그인해서 토큰 획득
    login_data = {
        "std_id": "12345678",
        "password": "test1234",
        "type": 0,
        "account_register": False,
        "data": ""
    }
    
    response = client.post("/account/action", json=login_data)
    first_login_data = response.json()
    token = first_login_data["new_token"]
    
    # 토큰으로 로그인
    token_login_data = {
        "std_id": "12345678",
        "password": token,
        "type": 0,
        "account_register": False,
        "data": "",
        "force_new_data": False
    }
    
    # API 호출
    response = client.post("/account/action", json=token_login_data)
    assert response.status_code == 200
    
    # 응답 검증
    data = response.json()
    assert data["success"] is True


def test_update_data(client, test_db, test_token_cache):
    """사용자 데이터 업데이트 테스트"""
    # 테스트 사용자 생성
    test_user = schemas.UserCreate(
        username="12345678",
        password="test1234"
    )
    user = crud.create_user(db=test_db, user=test_user)
    
    # 로그인해서 토큰 획득
    login_data = {
        "std_id": "12345678",
        "password": "test1234",
        "type": 0,
        "account_register": False,
        "data": ""
    }
    
    response = client.post("/account/action", json=login_data)
    login_response = response.json()
    token = login_response["new_token"]
    
    # 데이터 업데이트
    test_data = json.dumps([{"id": 1, "name": "Test Data"}])
    update_data = {
        "std_id": "12345678",
        "password": token,
        "type": 1,  # 업데이트 타입
        "account_register": False,
        "data": test_data
    }
    
    # API 호출
    response = client.post("/account/action", json=update_data)
    assert response.status_code == 200
    
    # 응답 검증
    data = response.json()
    assert data["success"] is True
    
    # 다시 조회하여 데이터가 업데이트 되었는지 확인
    get_data = {
        "std_id": "12345678",
        "password": token,
        "type": 0,
        "account_register": False,
        "data": "",
        "force_new_data": True
    }
    
    response = client.post("/account/action", json=get_data)
    data = response.json()
    assert data["data"] == test_data


def test_change_password(client, test_db):
    """비밀번호 변경 테스트"""
    # 테스트 사용자 생성
    test_user = schemas.UserCreate(
        username="12345678",
        password="test1234"
    )
    user = crud.create_user(db=test_db, user=test_user)
    
    # 비밀번호 변경 데이터
    change_pw_data = {
        "std_id": "12345678",
        "password": "test1234",
        "new_password": "newtest5678"
    }
    
    # API 호출
    response = client.post("/account/change_password", json=change_pw_data)
    assert response.status_code == 200
    
    # 응답 검증
    data = response.json()
    assert data["success"] is True
    
    # 새 비밀번호로 로그인 가능한지 확인
    login_data = {
        "std_id": "12345678",
        "password": "newtest5678",
        "type": 0,
        "account_register": False,
        "data": ""
    }
    
    response = client.post("/account/action", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
