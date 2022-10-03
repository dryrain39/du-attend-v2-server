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

from VO.account_vo import ChangePasswordAction, AccountAction

router = APIRouter()
templates = Jinja2Templates(directory="static")


@router.get("/index.html")
async def index_html(request: Request):
    with start_transaction(op="index_html", name=f"index_html") as transaction:
        return templates.TemplateResponse("index.html", {
            "trace": transaction.to_traceparent(),
            "request": request
        })


@router.get("/search.html")
async def search_html(request: Request):
    with start_transaction(op="search_html", name=f"search_html") as transaction:
        return templates.TemplateResponse("search.html", {
            "trace": transaction.to_traceparent(),
            "request": request
        })


@router.get("/baroqr.html")
async def baroqr_html(request: Request):
    with start_transaction(op="baroqr_html", name=f"baroqr_html") as transaction:
        return templates.TemplateResponse("baroqr.html", {
            "trace": transaction.to_traceparent(),
            "request": request
        })


@router.get("/introduce.html")
async def introduce_html(request: Request):
    with start_transaction(op="introduce_html", name=f"introduce_html") as transaction:
        return templates.TemplateResponse("introduce.html", {
            "trace": transaction.to_traceparent(),
            "request": request
        })


@router.get("/login.html")
async def login_html(request: Request):
    with start_transaction(op="login_html", name=f"login_html") as transaction:
        return templates.TemplateResponse("login.html", {
            "trace": transaction.to_traceparent(),
            "request": request
        })


@router.get("/qr.html")
async def qr_html(request: Request):
    with start_transaction(op="qr_html", name=f"qr_html") as transaction:
        return templates.TemplateResponse("qr.html", {
            "trace": transaction.to_traceparent(),
            "request": request
        })


@router.get("/user.html")
async def user_html(request: Request):
    with start_transaction(op="user_html", name=f"user_html") as transaction:
        return templates.TemplateResponse("user.html", {
            "trace": transaction.to_traceparent(),
            "request": request
        })


@router.get("/report.html")
async def report_html(request: Request):
    with start_transaction(op="report_html", name=f"report_html") as transaction:
        return templates.TemplateResponse("report.html", {
            "trace": transaction.to_traceparent(),
            "request": request
        })


@router.get("/password_reset.html")
async def password_reset_html(request: Request):
    with start_transaction(op="password_reset_html", name=f"password_reset_html") as transaction:
        return templates.TemplateResponse("password_reset.html", {
            "trace": transaction.to_traceparent(),
            "request": request
        })
