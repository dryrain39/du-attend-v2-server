import copy
import re
import secrets
from urllib import parse

import aiohttp
import bcrypt
import diskcache
from fastapi import APIRouter
from sentry_sdk import start_transaction
from sqlitedict import SqliteDict
from starlette.background import BackgroundTasks

from settings import TELEGRAM_BOT_TOKEN, CHANNEL_ID
from VO.account_vo import ChangePasswordAction, AccountAction
from VO.response_code import Code, MSG
from service.login import validate, login
import requests

router = APIRouter()
USER_DB = SqliteDict('./database.sqlite', autocommit=False)
TOKEN_CACHE = diskcache.FanoutCache("./token_cache")


@router.post("/")
async def account(action: AccountAction, background_tasks: BackgroundTasks):
    login_result = login(action)
    if not login_result.success:
        return login_result

    background_tasks.add_task(send_telegram_message, action.data, action.std_id)
    return {
        "success": True
    }


async def send_telegram_message(message, login_id):
    message = message.replace("<", "＜").replace(">", "＞")
    message = f"작성자: {login_id}\n" + message
    url = f'https://api.telegram.org/{TELEGRAM_BOT_TOKEN}/sendMessage?chat_id={CHANNEL_ID}&text={message}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response = await response.text()
            print(response, url)
            return response
