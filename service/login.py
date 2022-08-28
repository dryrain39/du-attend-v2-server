import copy
import os
import re
import secrets
import shutil
from typing import Tuple

import bcrypt
import diskcache
from fastapi import APIRouter
from sentry_sdk import start_transaction, start_span
from sqlitedict import SqliteDict
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from VO.account_vo import ChangePasswordAction, AccountAction, LoginResponse

# 사용자 로그인에 필요한 데이터
from config.config import USER_DB_PATH

USER_DB = SqliteDict(USER_DB_PATH, autocommit=False)
TOKEN_CACHE = diskcache.FanoutCache("./token_cache")


def validate(std_id, password) -> Tuple[bool, LoginResponse]:
    if not re.match(r"^[0-9]{8}$", std_id):
        return False, LoginResponse(success=False, code="IDINVALID", message="ID 는 학번이여야 합니다.")

    if len(password) > 36 or len(password) < 4:
        return False, LoginResponse(success=False, code="PWINVALID", message="비밀번호는 4 ~ 36 자리로 입력해 주십시오.")

    return True, LoginResponse(success=False, code="Validate success.", message="")


def login(action: AccountAction) -> LoginResponse:
    validate_result, msg = validate(action.std_id, action.password)
    if not validate_result:
        return msg

    login_by_token = False
    new_token = None
    user_password = USER_DB.get(action.std_id, {}).get("password", None)
    # 토큰으로 체크 또는 암호로 체크

    if user_password is None:
        return LoginResponse(success=False, code="PWDIDNOTMATCH", message="암호가 다릅니다.")


    # 암호가 맞지 않으면
    if not bcrypt.checkpw(action.password.encode(), user_password):
        # 토큰 데이터베이스에서 확인
        if TOKEN_CACHE.get(action.password, None) != user_password:
            return LoginResponse(success=False, code="PWDIDNOTMATCH", message="암호가 다릅니다.")
        login_by_token = True

    # 암호로 로그인했으면 토큰을 등록해준다
    if not login_by_token:
        new_token = secrets.token_urlsafe(16)
        new_token = new_token
        TOKEN_CACHE.add(key=new_token, value=USER_DB[action.std_id]["password"], expire=604800)  # 604800 = 7 days

    return LoginResponse(success=True, code="LOGINOK", message="인증되었습니다.", new_token=new_token)
