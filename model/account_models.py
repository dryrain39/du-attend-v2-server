from typing import Optional

from pydantic import BaseModel


class AccountAction(BaseModel):
    std_id: str
    password: str
    type: int
    data: Optional[str] = ""
    account_register: Optional[bool] = None


class ChangePasswordAction(BaseModel):
    std_id: str
    password: str
    new_password: str