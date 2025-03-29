from fastapi import APIRouter

import route.user.account as account
import route.user.account_v2 as account_v2

import route.qr.decode as qr_decode
import route.html.html as html
import route.user.bug_report as bug_report

import route.user.user_v3 as user_v2

import route.misc.version as version
import route.misc.redirectRouter as redirect_router
import route.misc.outlink_router as outlink_router


api_router = APIRouter()

api_router.include_router(account_v2.router, prefix='/account', tags=['account'])
api_router.include_router(qr_decode.router, prefix='', tags=['qr_decode'])
api_router.include_router(html.router, prefix='/static', tags=['html'])
api_router.include_router(bug_report.router, prefix='/report', tags=['report'])

# api_router.include_router(user_v2.router, prefix='/account/v2', tags=['account'])

api_router.include_router(version.router, prefix='/version', tags=['version'])

api_router.include_router(outlink_router.router, prefix='/out', tags=['out'])

