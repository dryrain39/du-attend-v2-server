from typing import Optional

from fastapi import Depends
from sqlalchemy.orm import Session

import schemas.log_schemas as schemas
import entity.log_entity as models
from database.db import get_session
from entity.user_entity import User
from enums.logtype import LogType
from service.user_deps import get_token_from_cookie


def put_log(db: Session, log_sch: schemas.LogInsert):
    db_log = models.Log(
        username=log_sch.username,
        type=str(log_sch.type.value),
        attr=log_sch.attr,
        sub_attr=log_sch.sub_attr
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


class LogInsertService:

    def __init__(self, db: Session = Depends(get_session), user_info: Optional[User] = Depends(get_token_from_cookie)):
        print("log insert init")
        self.db = db

        self.user = None
        self.username = None

        if user_info is not None:
            self.user = user_info
            self.username = user_info.username

    def insert(self, log_sch: schemas.LogInsert):
        print("log insert insert")

        db = self.db

        if log_sch.username is None and self.username is not None:
            log_sch.username = self.username

        # 방문자의 경우 로그인 되어있지 않으면 기록 안 함
        if log_sch.type == LogType.VISIT and self.username is None:
            return

        db_log = models.Log(
            username=log_sch.username,
            type=str(log_sch.type.value),
            attr=log_sch.attr,
            sub_attr=log_sch.sub_attr
        )
        db.add(db_log)
        db.commit()
        db.refresh(db_log)
        return db_log

    def close(self):
        pass
