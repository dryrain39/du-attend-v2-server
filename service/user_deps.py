from typing import Optional

from fastapi import Cookie

from entity.user_entity import User
from util.user_util import get_user_by_jwt_token


def get_token_from_cookie(token: Optional[str] = Cookie(None)) -> Optional[User]:
    if token is None:
        return None

    return get_user_by_jwt_token(token)
