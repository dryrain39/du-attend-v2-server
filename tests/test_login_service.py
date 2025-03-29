import pytest
from service.login import validate, login
from VO.account_vo import AccountAction, LoginResponse
from schemas.user_schemas import UserCreate
import service.user_service as crud
from util.user_util import encode_jwt_token


def test_validate_valid_input():
    """유효한 입력값 검증 테스트"""
    # 유효한 학번과 비밀번호
    is_valid, response = validate("12345678", "validPassword")
    assert is_valid is True
    assert response.success is False  # validate는 성공해도 success=False 반환
    assert response.code == "Validate success."


def test_validate_invalid_id():
    """유효하지 않은 학번 검증 테스트"""
    # 학번이 숫자 8자리가 아닌 경우
    is_valid, response = validate("123", "password")
    assert is_valid is False
    assert response.success is False
    assert response.code == "IDINVALID"
    
    is_valid, response = validate("abcdefgh", "password")
    assert is_valid is False
    assert response.success is False
    assert response.code == "IDINVALID"


def test_validate_invalid_password():
    """유효하지 않은 비밀번호 검증 테스트"""
    # 비밀번호가 4자리 미만인 경우
    is_valid, response = validate("12345678", "123")
    assert is_valid is False
    assert response.success is False
    assert response.code == "PWINVALID"


def test_login_success(test_db):
    """로그인 성공 테스트"""
    # 테스트 사용자 생성
    user = crud.create_user(
        db=test_db, 
        user=UserCreate(username="12345678", password="test1234")
    )
    
    # 로그인 시도
    action = AccountAction(
        std_id="12345678",
        password="test1234",
        type=0,
        account_register=False,
        data=""
    )
    
    response = login(action, test_db)
    assert response.success is True
    assert response.code == "LOGINOK"
    assert response.new_token is not None  # 새 토큰 발급 확인


def test_login_fail_invalid_password(test_db):
    """잘못된 비밀번호로 로그인 실패 테스트"""
    # 테스트 사용자 생성
    user = crud.create_user(
        db=test_db, 
        user=UserCreate(username="12345678", password="test1234")
    )
    
    # 잘못된 비밀번호로 로그인 시도
    action = AccountAction(
        std_id="12345678",
        password="wrong_password",
        type=0,
        account_register=False,
        data=""
    )
    
    response = login(action, test_db)
    assert response.success is False
    assert response.code == "PWDIDNOTMATCH"


def test_login_with_token(test_db):
    """JWT 토큰을 사용한 로그인 테스트"""
    # 테스트 사용자 생성
    user = crud.create_user(
        db=test_db, 
        user=UserCreate(username="12345678", password="test1234")
    )
    
    # 토큰 생성
    token = encode_jwt_token(user)
    
    # 토큰으로 로그인 시도
    action = AccountAction(
        std_id="12345678",
        password=token,
        type=0,
        account_register=False,
        data=""
    )
    
    response = login(action, test_db)
    assert response.success is True
    assert response.code == "LOGINOK"
