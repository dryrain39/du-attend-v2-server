import copy
import re
import secrets

import bcrypt
import diskcache
from fastapi import APIRouter
from sentry_sdk import start_transaction
from sqlitedict import SqliteDict

from VO.account_vo import ChangePasswordAction, AccountAction
from VO.response_code import Code, MSG

router = APIRouter()
USER_DB = SqliteDict('./database.sqlite', autocommit=False)
TOKEN_CACHE = diskcache.FanoutCache("./token_cache")


def validate(std_id, password):
    if not re.match(r"^[0-9]{8}$", std_id):
        return False, {"success": False, "code": Code.INVALID_ID, "message": MSG.INVALID_ID}

    if len(password) > 36 or len(password) < 4:
        return False, {"success": False, "code": Code.INVALID_PW, "message": MSG.INVALID_PW}

    return True, {}


@router.post("/change_password")
async def change_password(action: ChangePasswordAction):
    validate_result, msg = validate(action.std_id, action.password)
    if not validate_result:
        return msg

    validate_result, msg = validate(action.std_id, action.new_password)
    if not validate_result:
        return msg

    if not USER_DB.get(action.std_id, False):
        return {"success": False, "code": Code.ID_NOT_FOUND, "message": MSG.ID_NOT_FOUND}
    else:
        user_password = USER_DB[action.std_id]["password"]
        # 암호로 체크
        if not bcrypt.checkpw(action.password.encode(), user_password):
            return {"success": False, "code": Code.PW_NOT_MATCH, "message": MSG.PW_NOT_MATCH}

    user_info = USER_DB[action.std_id]
    user_info["password"] = bcrypt.hashpw(action.new_password.encode(), bcrypt.gensalt(4))
    USER_DB[action.std_id] = user_info

    USER_DB.commit()

    return {"success": True}


@router.post("/action")
async def account(action: AccountAction):
    validate_result, msg = validate(action.std_id, action.password)
    if not validate_result:
        return msg

    login_by_token = False

    if not USER_DB.get(action.std_id, False):

        if not action.account_register:
            return {"success": False, "code": Code.ID_NOT_FOUND, "message": MSG.ID_NOT_FOUND}

        USER_DB[action.std_id] = {
            "password": bcrypt.hashpw(action.password.encode(), bcrypt.gensalt(4)),
            "data": "",
        }
    else:
        user_password = USER_DB[action.std_id]["password"]
        # 토큰으로 체크 또는 암호로 체크

        if not bcrypt.checkpw(action.password.encode(), user_password):
            if TOKEN_CACHE.get(action.password, None) != user_password:
                return {"success": False, "code": Code.PW_NOT_MATCH, "message": MSG.PW_NOT_MATCH}
            login_by_token = True

    if action.type == 1:
        account_data = USER_DB[action.std_id]
        account_data["data"] = str(action.data)
        USER_DB[action.std_id] = account_data

    ret = {"success": True, "data": copy.deepcopy(USER_DB[action.std_id]["data"])}

    # 암호로 로그인했으면 토큰을 등록해준다
    if not login_by_token:
        new_token = secrets.token_urlsafe(16)
        ret["new_token"] = new_token
        TOKEN_CACHE.add(key=new_token, value=USER_DB[action.std_id]["password"], expire=604800)  # 604800 = 7 days

    USER_DB.commit()
    # token_cache.close()

    return ret
