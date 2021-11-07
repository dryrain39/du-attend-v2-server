import secrets
import base64
import copy
import time

import bcrypt
from typing import *
from Crypto.Cipher import AES
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
import diskcache
from settings import *
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlitedict import SqliteDict
import re

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

TOKEN_CACHE = diskcache.FanoutCache("./token_cache")
QR_DECODE_CACHE = diskcache.FanoutCache("./qr_cache")
USER_DB = SqliteDict('./database.sqlite', autocommit=False)

origins = [
    "http://dryrain39.github.io",
    "https://dryrain39.github.io",
    "http://kpc",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def validate(std_id, password):
    if not re.match(r"^[0-9]{8}$", std_id):
        return False, {"success": False, "code": "IDINVALID", "message": "ID 는 학번이여야 합니다."}

    if len(password) > 36 or len(password) < 4:
        return False, {"success": False, "code": "PWINVALID", "message": "비밀번호는 4 ~ 36 자리로 입력해 주세요."}

    return True, {}


def _unpad(s):
    return s[:-ord(s[len(s) - 1:])]


class AccountAction(BaseModel):
    std_id: str
    password: str
    type: int
    data: Optional[str] = ""
    account_register: Optional[bool] = None


class ChangePasswordAction(BaseModel):
    std_id: str
    password: str
    new_password: str


@app.post("/account/change_password")
async def change_password(action: ChangePasswordAction):
    if not USER_DB.get(action.std_id, False):
        return {"success": False, "code": "NOACCOUNT", "message": "회원정보가 없습니다."}
    else:
        user_password = USER_DB[action.std_id]["password"]
        # 암호로 체크
        if not bcrypt.checkpw(action.password.encode(), user_password):
            return {"success": False, "code": "PWDIDNOTMATCH", "message": "암호가 다릅니다."}

    user_info = USER_DB[action.std_id]
    user_info["password"] = bcrypt.hashpw(action.new_password.encode(), bcrypt.gensalt(4))
    USER_DB[action.std_id] = user_info

    USER_DB.commit()

    return {"success": True}


@app.post("/account/action")
async def account(action: AccountAction):
    validate_result, msg = validate(action.std_id, action.password)
    if not validate_result:
        return msg

    login_by_token = False

    if not USER_DB.get(action.std_id, False):
        if not action.account_register:
            return {"success": False, "code": "NOACCOUNT", "message": "회원정보가 없습니다."}

        USER_DB[action.std_id] = {
            "password": bcrypt.hashpw(action.password.encode(), bcrypt.gensalt(4)),
            "data": "",
        }
    else:
        user_password = USER_DB[action.std_id]["password"]
        # 토큰으로 체크 또는 암호로 체크

        if not bcrypt.checkpw(action.password.encode(), user_password):
            if TOKEN_CACHE.get(action.password, None) != user_password:
                return {"success": False, "code": "PWDIDNOTMATCH", "message": "암호가 다릅니다."}
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


@QR_DECODE_CACHE.memoize(typed=True, expire=86400)
def decode_data(qr_string: str):
    qr_encrypted = bytes.fromhex(qr_string)

    cipher = AES.new(KEY, AES.MODE_ECB)
    qr_data = _unpad(cipher.decrypt(qr_encrypted)).decode('utf-8')
    return qr_data


@app.get("/attend_url")
async def decode(qr_string: str, std_id: str):
    try:
        qr_data = decode_data(qr_string)
        nfc_data = base64.b64encode(qr_data.encode()).decode("utf-8")
        std_id = base64.b64encode(std_id.encode()).decode("utf-8")
    except Exception as e:
        return {"message": "뒤로가기 후 다시 시도해 주세요."}

    parameter = f"?sno={std_id}&nfc={nfc_data}&type=UQ==&gpsLati=MA==&gpsLong=MA==&time_stamp=%7BtimeStamp%7D&pgmNew=Y"
    return RedirectResponse(url='http://attend.daegu.ac.kr:8081/web/std/checkAttend.do' + parameter)


@app.get("/7qy38tiejfkdnojiwgu9eyhijdfk")
async def server_checker():
    return {"message": "Hello World"}


@app.get("/")
async def root():
    return RedirectResponse(url='/static/index.html')
