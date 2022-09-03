import copy
import os
import re
import secrets
import shutil
from typing import Tuple

import bcrypt
import diskcache
from fastapi import APIRouter, Depends
from sentry_sdk import start_transaction, start_span
from sqlalchemy.orm import Session
from sqlitedict import SqliteDict
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from VO.account_vo import ChangePasswordAction, AccountAction, LoginResponse

# 사용자 로그인에 필요한 데이터
from config.config import USER_DB_PATH
from database.db import get_session

import schemas.user_schemas as schemas
import entity.user_entity as models
import service.user_service as crud
from util.user_util import get_user_by_jwt_token, check_password, encode_jwt_token

USER_DB = SqliteDict(USER_DB_PATH, autocommit=False)
TOKEN_CACHE = diskcache.FanoutCache("./token_cache")


def validate(std_id, password) -> Tuple[bool, LoginResponse]:
    if not re.match(r"^[0-9]{8}$", std_id):
        return False, LoginResponse(success=False, code="IDINVALID", message="ID 는 학번이여야 합니다.")

    if len(password) < 4:
        return False, LoginResponse(success=False, code="PWINVALID", message="비밀번호는 4 ~ 36 자리로 입력해 주십시오.")

    return True, LoginResponse(success=False, code="Validate success.", message="")


def login(action: AccountAction, db: Session) -> LoginResponse:
    validate_result, msg = validate(action.std_id, action.password)
    if not validate_result:
        return msg

    jwt_token_data: models.User = get_user_by_jwt_token(action.password)
    if jwt_token_data is not None:
        # 비밀번호가 토큰인경우
        print(f"{action.std_id} 토큰 인증되었습니다.")
        return LoginResponse(success=True, code="LOGINOK", message="로그인 성공.")
    else:
        # 비밀번호인경우
        # 토큰이 아닌 경우 & cache 가 오래된 경우
        user_info: models.User = crud.get_user_by_username(db, username=action.std_id)

        if user_info is None:
            return LoginResponse(success=False, code="PWDIDNOTMATCH", message="암호가 다릅니다. 다시 로그인 해주세요.")

        # 암호 체크
        if not check_password(password=action.password, hashed_password=user_info.password):
            return LoginResponse(success=False, code="PWDIDNOTMATCH", message="암호가 다릅니다. 다시 로그인 해주세요.")

        # 로그인 성공
        return LoginResponse(success=True, code="LOGINOK", message="로그인 성공.", new_token=encode_jwt_token(user_info))
