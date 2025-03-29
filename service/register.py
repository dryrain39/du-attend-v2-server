import re
from typing import Tuple
import diskcache
from fastapi import Depends
from sqlalchemy.orm import Session

from VO.account_vo import AccountAction, LoginResponse
from VO.response_code import Code, MSG
from database.db import get_session
import service.user_service as crud

# SqliteDict 제거
TOKEN_CACHE = diskcache.FanoutCache("./token_cache")


def validate(std_id, password) -> Tuple[bool, LoginResponse]:
    if not re.match(r"^[0-9]{8}$", std_id):
        return False, LoginResponse(success=False, code=Code.INVALID_ID, message=MSG.INVALID_ID)

    if len(password) > 36 or len(password) < 4:
        return False, LoginResponse(success=False, code=Code.INVALID_PW, message=MSG.INVALID_PW)

    return True, LoginResponse(success=False, code=Code.NOP, message=MSG.NOP)


def register(action: AccountAction, db: Session = Depends(get_session)) -> LoginResponse:
    validate_result, msg = validate(action.std_id, action.password)
    if not validate_result:
        return msg

    if not action.account_register:
        return LoginResponse(success=False, code=Code.INVALID_MODE, message=MSG.INVALID_MODE)

    db_user = crud.get_user_by_username(db, username=action.std_id)
    if db_user:
        return LoginResponse(success=False, code=Code.ID_EXISTS, message=MSG.ID_EXISTS)

    return LoginResponse(success=True, code=Code.REGISTER_OK, message=MSG.REGISTER_OK)
