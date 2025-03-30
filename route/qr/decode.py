import base64
import logging
from datetime import datetime, timedelta
from urllib.parse import quote

import diskcache
from fastapi import APIRouter, Depends
from Crypto.Cipher import AES
from sentry_sdk.tracing import Transaction
from starlette.background import BackgroundTasks
from starlette.requests import Request
from starlette.responses import RedirectResponse

from config.config import KEY
from enums.logtype import LogType
from schemas.log_schemas import LogInsert
from service.log_service import LogInsertService

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
async def decode(qr_string: str, std_id: str, request: Request, background_tasks: BackgroundTasks,
                 log_service: LogInsertService = Depends(LogInsertService)):
    try:
        qr_data = decode_data(qr_string)
        nfc_data = base64.b64encode(qr_data.encode()).decode("utf-8")
        std_id_enc = base64.b64encode(std_id.encode()).decode("utf-8")
    except Exception as e:
        logging.exception(e, exc_info=True)
        return {"message": "뒤로가기 후 다시 시도해 주세요."}

    # Get the current UTC date and time
    now_utc = datetime.utcnow()

    # Convert UTC time to KST
    now_kst = now_utc + timedelta(hours=9)

    # Format the date and time to the required string format
    formatted_date = now_kst.strftime('%Y-%m-%dT%H:%M:%S.') + f'{now_kst.microsecond // 1000:03d}Z'
    encoded_date = quote(formatted_date)

    parameter = f"?sno={std_id_enc}&nfc={nfc_data}&type=UQ%3D%3D&gpsLati=MA%3D%3D&gpsLong=MA%3D%3D&time_stamp={encoded_date}&ver=24]"
    background_tasks.add_task(log_service.insert,
                              LogInsert(type=LogType.ATTEND, username=f"{std_id}", attr=f"{qr_data}",
                                        sub_attr=f"{qr_string}"))
    return RedirectResponse(url='https://attend.daegu.ac.kr:8082/web/std/checkAttend.do' + parameter)
