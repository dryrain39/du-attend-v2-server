import copy
import re
import secrets

import bcrypt
import diskcache
from fastapi import APIRouter, Depends
from sentry_sdk import start_transaction
from sqlalchemy.orm import Session
from sqlitedict import SqliteDict

from VO.account_vo import ChangePasswordAction, AccountAction
from VO.response_code import Code, MSG
from config.config import USER_DB_PATH
from database.db import get_session
from schemas.cache_data import CacheData
from util.user_util import decode_jwt_token, get_user_by_jwt_token, check_password, encode_jwt_token
import schemas.user_schemas as schemas
import entity.user_entity as models
import service.user_service as crud

router = APIRouter()
USER_DB = SqliteDict(USER_DB_PATH, autocommit=False)
TOKEN_CACHE = diskcache.FanoutCache("./token_cache")


def validate(std_id, password):
    if not re.match(r"^[0-9]{8}$", std_id):
        return False, {"success": False, "code": Code.INVALID_ID, "message": MSG.INVALID_ID}

    if len(password) < 4:
        return False, {"success": False, "code": Code.INVALID_PW, "message": MSG.INVALID_PW}

    return True, {}


@router.post("/change_password")
async def change_password(action: ChangePasswordAction, db: Session = Depends(get_session)):
    validate_result, msg = validate(action.std_id, action.password)
    if not validate_result:
        return msg

    validate_result, msg = validate(action.std_id, action.new_password)
    if not validate_result:
        return msg

    user_info: models.User = crud.get_user_by_username(db, username=action.std_id)

    if user_info is None:
        return {"success": False, "code": Code.ID_NOT_FOUND, "message": MSG.ID_NOT_FOUND}

    # 암호 체크
    if not check_password(password=action.password, hashed_password=user_info.password):
        return {"success": False, "code": Code.PW_NOT_MATCH, "message": MSG.PW_NOT_MATCH}

    crud.update_user_by_username(
        db,
        username=user_info.username,
        user_update=schemas.UserUpdate(password=action.new_password)
    )

    return {"success": True}


@router.post("/action")
async def account(action: AccountAction, db: Session = Depends(get_session)):
    print(action)

    validate_result, msg = validate(action.std_id, action.password)
    if not validate_result:
        return msg

    # 계정 등록인 경우
    if action.type == 0 and action.account_register:
        db_user = crud.get_user_by_username(db, username=action.std_id)
        if db_user:
            return {"success": False, "code": Code.ID_EXISTS, "message": MSG.ID_EXISTS}

        new_user = crud.create_user(db=db, user=schemas.UserCreate(username=action.std_id, password=action.password))

        return {
            "success": True,
            "data": "[]",
            "new_token": encode_jwt_token(new_user)
        }

    # 로그인인 경우
    jwt_token_data: models.User = get_user_by_jwt_token(action.password)
    if jwt_token_data is not None:
        # 비밀번호가 토큰인경우
        print(f"{action.std_id} 토큰 인증되었습니다.")

        # cache 에서 data 불러오기
        cached_data: CacheData = TOKEN_CACHE.get(f"attend_data_{action.std_id}")
        is_cache_valid = cached_data and cached_data.updated_time >= jwt_token_data.updated_time
        is_token_outdated = cached_data and cached_data.updated_time > jwt_token_data.updated_time

        if (cached_data is not None) and is_cache_valid and action.type == 0:
            print(f"{is_cache_valid} {cached_data.updated_time} {jwt_token_data.updated_time}")
            # 깨진 데이터의 경우
            if cached_data.data is None or cached_data.data == "":
                cached_data.data = "[]"

            ret = {"success": True, "data": cached_data.data}

            if is_token_outdated:
                jwt_token_data.updated_time = cached_data.updated_time
                ret["new_token"] = encode_jwt_token(jwt_token_data)

            return ret
        else:
            print(f"{action.std_id} 캐시가 너무 오래됨. 또는 action type 이 1임.")
            user_info: models.User = crud.get_user_by_username(db, username=jwt_token_data.username)

            if not user_info:
                print("유저 정보가 없습니다.")
                return {"success": False, "code": Code.ID_NOT_FOUND, "message": MSG.ID_NOT_FOUND}
    else:
        # 비밀번호인경우
        # 토큰이 아닌 경우 & cache 가 오래된 경우
        user_info: models.User = crud.get_user_by_username(db, username=action.std_id)

        if user_info is None:
            return {"success": False, "code": Code.ID_NOT_FOUND, "message": MSG.ID_NOT_FOUND}

        # 암호 체크
        if not check_password(password=action.password, hashed_password=user_info.password):
            return {"success": False, "code": Code.PW_NOT_MATCH, "message": MSG.PW_NOT_MATCH}

    # 로그인 성공

    # 업데이트의 경우
    if action.type == 1:
        print("업데이트 작업 시작, 기존:", user_info.updated_time)
        crud.update_user_by_username(
            db,
            username=user_info.username,
            user_update=schemas.UserUpdate(attend_data=action.data)
        )

        db.close()
        user_info: models.User = crud.get_user_by_username(db, username=action.std_id)

        print("업데이트 작업 완료, 새로운:", user_info.updated_time)
        pass

    # 깨진 데이터의 경우
    if user_info.attend_data is None or user_info.attend_data == "":
        user_info.attend_data = "[]"

    # 캐시 저장
    TOKEN_CACHE.set(f"attend_data_{action.std_id}",
                    CacheData(data=user_info.attend_data, updated_time=user_info.updated_time))

    return {
        "success": True,
        "data": user_info.attend_data,
        "new_token": encode_jwt_token(user_info)
    }
