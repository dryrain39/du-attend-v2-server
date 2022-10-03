import dataclasses
from typing import Optional
from pydantic import BaseModel


class AccountAction(BaseModel):
    std_id: str
    password: str
    type: int  # 1: modify data
    data: Optional[str] = ""
    account_register: Optional[bool] = None
    force_new_data: Optional[bool] = None


class ChangePasswordAction(BaseModel):
    std_id: str
    password: str
    new_password: str


@dataclasses.dataclass
class LoginResponse():
    success: bool
    code: Optional[str] = ""
    message: Optional[str] = ""
    new_token: Optional[str] = None
