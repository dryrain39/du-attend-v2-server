from fastapi import APIRouter

import route.user.account as account
import route.qr.decode as qr_decode
import route.html.html as html

api_router = APIRouter()

api_router.include_router(account.router, prefix='/account', tags=['account'])
api_router.include_router(qr_decode.router, prefix='', tags=['qr_decode'])
api_router.include_router(html.router, prefix='/static', tags=['html'])
