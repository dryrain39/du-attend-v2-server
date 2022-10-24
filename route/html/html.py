import copy
import re
import secrets

import bcrypt
import diskcache
from fastapi import APIRouter, Depends
from sentry_sdk import start_transaction, start_span
from sqlitedict import SqliteDict
from starlette.background import BackgroundTasks
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from VO.account_vo import ChangePasswordAction, AccountAction
from enums.logtype import LogType
from schemas.log_schemas import LogInsert
from service.log_service import LogInsertService

router = APIRouter()
templates = Jinja2Templates(directory="static")


@router.get("/index.html")
async def index_html(request: Request, background_tasks: BackgroundTasks,
                     log_service: LogInsertService = Depends(LogInsertService)):
    background_tasks.add_task(log_service.insert, LogInsert(type=LogType.VISIT, attr="index"))
    return templates.TemplateResponse("index.html", {
        "trace": "",
        "request": request
    })


@router.get("/search.html")
async def search_html(request: Request, background_tasks: BackgroundTasks,
                      log_service: LogInsertService = Depends(LogInsertService)):
    background_tasks.add_task(log_service.insert, LogInsert(type=LogType.VISIT, attr="search",
                                                            sub_attr=request.query_params.get("q", None)))
    return templates.TemplateResponse("search.html", {
        "trace": "",
        "request": request
    })


@router.get("/baroqr.html")
async def baroqr_html(request: Request, background_tasks: BackgroundTasks,
                      log_service: LogInsertService = Depends(LogInsertService)):
    background_tasks.add_task(log_service.insert, LogInsert(type=LogType.VISIT, attr="baroqr"))
    return templates.TemplateResponse("baroqr.html", {
        "trace": "",
        "request": request
    })


@router.get("/introduce.html")
async def introduce_html(request: Request, background_tasks: BackgroundTasks,
                         log_service: LogInsertService = Depends(LogInsertService)):
    background_tasks.add_task(log_service.insert, LogInsert(type=LogType.VISIT, attr="introduce"))
    return templates.TemplateResponse("introduce.html", {
        "trace": "",
        "request": request
    })


@router.get("/login.html")
async def login_html(request: Request, background_tasks: BackgroundTasks,
                     log_service: LogInsertService = Depends(LogInsertService)):
    background_tasks.add_task(log_service.insert, LogInsert(type=LogType.VISIT, attr="login"))
    return templates.TemplateResponse("login.html", {
        "trace": "",
        "request": request
    })


@router.get("/qr.html")
async def qr_html(request: Request, background_tasks: BackgroundTasks,
                  log_service: LogInsertService = Depends(LogInsertService)):
    background_tasks.add_task(log_service.insert, LogInsert(type=LogType.VISIT, attr="qr"))
    return templates.TemplateResponse("qr.html", {
        "trace": "",
        "request": request
    })


@router.get("/user.html")
async def user_html(request: Request, background_tasks: BackgroundTasks,
                    log_service: LogInsertService = Depends(LogInsertService)):
    background_tasks.add_task(log_service.insert, LogInsert(type=LogType.VISIT, attr="user"))
    return templates.TemplateResponse("user.html", {
        "trace": "",
        "request": request
    })


@router.get("/report.html")
async def report_html(request: Request, background_tasks: BackgroundTasks,
                      log_service: LogInsertService = Depends(LogInsertService)):
    background_tasks.add_task(log_service.insert, LogInsert(type=LogType.VISIT, attr="report"))
    return templates.TemplateResponse("report.html", {
        "trace": "",
        "request": request
    })


@router.get("/password_reset.html")
async def password_reset_html(request: Request, background_tasks: BackgroundTasks,
                              log_service: LogInsertService = Depends(LogInsertService)):
    background_tasks.add_task(log_service.insert, LogInsert(type=LogType.VISIT, attr="password_reset"))
    return templates.TemplateResponse("password_reset.html", {
        "trace": "",
        "request": request
    })
