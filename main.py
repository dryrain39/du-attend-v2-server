import secrets
import base64
import bcrypt
from typing import *
from Crypto.Cipher import AES
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from settings import *
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlitedict import SqliteDict
import re

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

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


@app.post("/account/action")
async def root(action: AccountAction):
    validate_result, msg = validate(action.std_id, action.password)
    if not validate_result:
        return msg

    db = SqliteDict('./database.sqlite', autocommit=False)

    if not db.get(action.std_id, False):
        if not action.account_register:
            return {"success": False, "code": "NOACCOUNT", "message": "회원정보가 없습니다."}

        db[action.std_id] = {
            "password": bcrypt.hashpw(action.password.encode(), bcrypt.gensalt(14)),
            "data": "",
        }
    else:
        if not bcrypt.checkpw(action.password.encode(), db[action.std_id]["password"]):
            return {"success": False, "code": "PWDIDNOTMATCH", "message": "암호가 다릅니다."}

    if action.type == 1:
        account_data = db[action.std_id]
        account_data["data"] = str(action.data)
        db[action.std_id] = account_data

    ret = {"success": True, "data": db[action.std_id]["data"]}
    db.commit()
    db.close()

    return ret


@app.get("/attend_url")
async def decode(qr_string: str, std_id: str):
    qr_encrypted = bytes.fromhex(qr_string)

    cipher = AES.new(KEY, AES.MODE_ECB)
    qr_data = _unpad(cipher.decrypt(qr_encrypted)).decode('utf-8')
    nfc_data = base64.b64encode(qr_data.encode()).decode("utf-8")
    std_id = base64.b64encode(std_id.encode()).decode("utf-8")

    parameter = f"?sno={std_id}&nfc={nfc_data}&type=UQ==&gpsLati=MA==&gpsLong=MA==&time_stamp=%7BtimeStamp%7D&pgmNew=Y"
    return RedirectResponse(url='http://attend.daegu.ac.kr:8081/web/std/checkAttend.do' + parameter)


@app.get("/7qy38tiejfkdnojiwgu9eyhijdfk")
async def server_checker():
    return {"message": "Hello World"}


@app.get("/")
async def root():
    return RedirectResponse(url='/static/index.html')
