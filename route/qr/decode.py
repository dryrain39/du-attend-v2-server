import base64
import logging

import diskcache
from fastapi import APIRouter
from Crypto.Cipher import AES
from sentry_sdk.tracing import Transaction
from starlette.requests import Request
from starlette.responses import RedirectResponse

from config.config import KEY

QR_DECODE_CACHE = diskcache.FanoutCache("./qr_cache")
router = APIRouter()


def _unpad(s):
    return s[:-ord(s[len(s) - 1:])]


def decode_data(qr_string: str):
    qr_encrypted = bytes.fromhex(qr_string)

    cipher = AES.new(KEY, AES.MODE_ECB)
    qr_data = _unpad(cipher.decrypt(qr_encrypted)).decode('utf-8')

    return qr_data


@router.get("/attend_url")
async def decode(qr_string: str, std_id: str, request: Request):
    with Transaction.continue_from_headers(request.headers, op="attend_jmp", name="attend_jmp") as transaction:
        try:
            qr_data = decode_data(qr_string)
            nfc_data = base64.b64encode(qr_data.encode()).decode("utf-8")
            std_id = base64.b64encode(std_id.encode()).decode("utf-8")
        except Exception as e:
            logging.exception(e, exc_info=True)
            return {"message": "뒤로가기 후 다시 시도해 주세요."}

        parameter = f"?sno={std_id}&nfc={nfc_data}&type=UQ==&gpsLati=MA==&gpsLong=MA==&time_stamp=%7BtimeStamp%7D&pgmNew=Y"
        transaction.finish()
        return RedirectResponse(url='http://attend.daegu.ac.kr:8081/web/std/checkAttend.do' + parameter)
