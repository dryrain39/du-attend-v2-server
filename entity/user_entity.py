import uuid
from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from fastapi_users import schemas
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, text, func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import declarative_mixin

from database.db import Base


@declarative_mixin
class TimestampMixin:
    """자동으로 업데이트 시간을 관리하는 믹스인"""
    
    @declared_attr
    def updated_time(cls):
        return Column(TIMESTAMP, nullable=False, 
                      server_default=text('CURRENT_TIMESTAMP'),
                      onupdate=func.current_timestamp())


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String, nullable=True)
    attend_data = Column(Text)
