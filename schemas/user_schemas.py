import datetime
from typing import List, Union, Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    attend_data: Optional[str]
    updated_time: Optional[datetime.datetime]


class UserUpdate(BaseModel):
    password: Optional[str]
    attend_data: Optional[str]


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
