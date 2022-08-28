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
from VO.response_code import Code, MSG
from config.config import USER_DB_PATH

USER_DB = SqliteDict(USER_DB_PATH, autocommit=False)
TOKEN_CACHE = diskcache.FanoutCache("./token_cache")


def validate(std_id, password) -> Tuple[bool, LoginResponse]:
    if not re.match(r"^[0-9]{8}$", std_id):
        return False, LoginResponse(success=False, code=Code.INVALID_ID, message=MSG.INVALID_ID)

    if len(password) > 36 or len(password) < 4:
        return False, LoginResponse(success=False, code=Code.INVALID_PW, message=MSG.INVALID_PW)

    return True, LoginResponse(success=False, code=Code.NOP, message=MSG.NOP)


def register(action: AccountAction) -> LoginResponse:
    validate_result, msg = validate(action.std_id, action.password)
    if not validate_result:
        return msg

    if not action.account_register:
        return LoginResponse(success=False, code=Code.INVALID_MODE, message=MSG.INVALID_MODE)

    if USER_DB.get(action.std_id, False):
        return LoginResponse(success=False, code=Code.ID_EXISTS, message=MSG.ID_EXISTS)

    USER_DB[action.std_id] = {
        "password": bcrypt.hashpw(action.password.encode(), bcrypt.gensalt(4)),
        "data": "",
    }

    USER_DB.commit()

    return LoginResponse(success=True, code=Code.REGISTER_OK, message=MSG.REGISTER_OK)
