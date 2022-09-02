import base64
import copy
import json
import os
import re
import secrets
import shutil

import bcrypt
import diskcache
from fastapi import APIRouter, HTTPException
from sentry_sdk import start_transaction, start_span
from sqlitedict import SqliteDict
from starlette.requests import Request
from starlette.responses import Response
from starlette.templating import Jinja2Templates

from VO.account_vo import ChangePasswordAction, AccountAction
from config.config import USER_DB_PATH
from fluent_logger.PromoFormat import PromoLogger, ActionCode
from route.user.account import validate
from service.login import login
from service.register import register
import logging

router = APIRouter()


@router.get("/")
async def get_version():
    version = "2022090301"
    try:
        node = os.uname().nodename
    except:
        node = "unknown"
    project_name = "attend.miscthings.net"

    return {
        "version": version,
        "node": node,
        "version_string": f"{node}.{version}.{project_name}"
    }
