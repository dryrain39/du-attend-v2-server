import aiohttp
import diskcache
from fastapi import APIRouter
from sqlitedict import SqliteDict
from starlette.background import BackgroundTasks
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from config.config import TELEGRAM_BOT_TOKEN, CHANNEL_ID, USER_DB_PATH
from VO.account_vo import AccountAction
from database.db import get_session
from service.login import login

import schemas.user_schemas as schemas
import entity.user_entity as models
import service.user_service as crud

router = APIRouter()


@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_session)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return crud.create_user(db=db, user=user)


@router.post("/wohash", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_session)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return crud.create_user_without_hash(db=db, user=user)


@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_session)):
    db_user = crud.get_user(db, user_id=user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    print(type(db_user))
    print(db_user.id)
    return db_user
