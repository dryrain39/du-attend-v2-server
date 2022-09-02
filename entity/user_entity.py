import uuid
from dataclasses import dataclass
from typing import Optional
from fastapi_users import schemas
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, text

from database.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String, nullable=True)

    updated_time = Column(TIMESTAMP, nullable=False,
                          server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    attend_data = Column(Text)
