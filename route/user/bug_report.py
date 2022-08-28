import aiohttp
import diskcache
from fastapi import APIRouter
from sqlitedict import SqliteDict
from starlette.background import BackgroundTasks

from config.config import TELEGRAM_BOT_TOKEN, CHANNEL_ID, USER_DB_PATH
from VO.account_vo import AccountAction
from service.login import login

router = APIRouter()
USER_DB = SqliteDict(USER_DB_PATH, autocommit=False)
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
    message = message.replace("\n", "%0A")
    url = f'https://api.telegram.org/{TELEGRAM_BOT_TOKEN}/sendMessage?chat_id={CHANNEL_ID}&text={message}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response = await response.text()
            print(response, url)
            return response
