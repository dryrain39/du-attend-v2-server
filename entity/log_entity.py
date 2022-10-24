import uuid
from dataclasses import dataclass
from typing import Optional
from fastapi_users import schemas
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, text

from database.db import Base


class Log(Base):
    __tablename__ = "attend_log"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=True, index=True)

    type = Column(String, index=True)
    attr = Column(String, nullable=True)
    sub_attr = Column(String, nullable=True)

    updated_time = Column(TIMESTAMP, nullable=False,
                          server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

