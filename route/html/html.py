import copy
import re
import secrets

import bcrypt
import diskcache
from fastapi import APIRouter
from sentry_sdk import start_transaction, start_span
from sqlitedict import SqliteDict
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from model.account_models import ChangePasswordAction, AccountAction

router = APIRouter()
templates = Jinja2Templates(directory="static")


@router.get("/index.html")
async def index_html(request: Request):
    with start_transaction(op="index_html", name=f"index_html") as transaction:
        return templates.TemplateResponse("index.html", {
            "trace": transaction.to_traceparent(),
            "request": request
        })


@router.get("/baroqr.html")
async def index_html(request: Request):
    with start_transaction(op="baroqr_html", name=f"baroqr_html") as transaction:
        return templates.TemplateResponse("baroqr.html", {
            "trace": transaction.to_traceparent(),
            "request": request
        })


@router.get("/introduce.html")
async def index_html(request: Request):
    with start_transaction(op="introduce_html", name=f"introduce_html") as transaction:
        return templates.TemplateResponse("introduce.html", {
            "trace": transaction.to_traceparent(),
            "request": request
        })


@router.get("/login.html")
async def index_html(request: Request):
    with start_transaction(op="login_html", name=f"login_html") as transaction:
        return templates.TemplateResponse("login.html", {
            "trace": transaction.to_traceparent(),
            "request": request
        })


@router.get("/qr.html")
async def index_html(request: Request):
    with start_transaction(op="qr_html", name=f"qr_html") as transaction:
        return templates.TemplateResponse("qr.html", {
            "trace": transaction.to_traceparent(),
            "request": request
        })


@router.get("/user.html")
async def index_html(request: Request):
    with start_transaction(op="user_html", name=f"user_html") as transaction:
        return templates.TemplateResponse("user.html", {
            "trace": transaction.to_traceparent(),
            "request": request
        })
