from fastapi import APIRouter

import route.user.account as account
import route.qr.decode as qr_decode
import route.html.html as html
import route.user.bug_report as bug_report

import route.promotion.promotion_22_04 as promotion_22_04

api_router = APIRouter()

api_router.include_router(account.router, prefix='/account', tags=['account'])
api_router.include_router(qr_decode.router, prefix='', tags=['qr_decode'])
api_router.include_router(html.router, prefix='/static', tags=['html'])
api_router.include_router(bug_report.router, prefix='/report', tags=['report'])

api_router.include_router(promotion_22_04.router, prefix='/2204', tags=['promotion'])
