from fastapi import Depends
from sqlalchemy.orm import Session

import schemas.log_schemas as schemas
import entity.log_entity as models
from database.db import get_session


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

    def __init__(self, db: Session = Depends(get_session)):
        print("log insert init")
        self.db = db

    def insert(self, log_sch: schemas.LogInsert):
        print("log insert insert")

        db = self.db
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
