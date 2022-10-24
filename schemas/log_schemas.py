import datetime
from typing import List, Union, Optional

from pydantic import BaseModel

from enums.logtype import LogType


class LogBase(BaseModel):
    username: Optional[str]

    type: LogType
    attr: Optional[str]
    sub_attr: Optional[str]

    updated_time: Optional[datetime.datetime]


class LogInsert(LogBase):
    pass


class Log(LogBase):
    class Config:
        orm_mode = True
