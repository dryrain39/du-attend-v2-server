import uuid
from dataclasses import dataclass
from typing import Optional
from fastapi_users import schemas
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, text, func
from sqlalchemy.ext.declarative import declared_attr

from database.db import Base
from entity.user_entity import TimestampMixin


class Log(Base, TimestampMixin):
    __tablename__ = "attend_log"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=True, index=True)

    type = Column(String, index=True)
    attr = Column(String, nullable=True)
    sub_attr = Column(String, nullable=True)


