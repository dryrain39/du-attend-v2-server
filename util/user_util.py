import datetime
from typing import Optional

import bcrypt
from jose import jwt
from jose.exceptions import JWTClaimsError, ExpiredSignatureError, JWTError

from config.config import KEY, JWT_KEY
from entity.user_entity import User


def hash_password(password: str):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(4)).decode()


def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def encode_jwt_token(user: User):
    token = jwt.encode({
        "iss": "attend.miscthings.net",
        "id": user.id,
        "username": user.username,
        "updated_time": user.updated_time.timestamp(),
        "exp": (datetime.datetime.utcnow() + datetime.timedelta(days=7)).timestamp()
    }, JWT_KEY, algorithm='HS256')
    return token


def get_user_by_jwt_token(token: str) -> Optional[User]:
    user_info = decode_jwt_token(token)
    if user_info is None:
        return None
    return User(id=user_info["id"], username=user_info["username"],
                updated_time=datetime.datetime.fromtimestamp(user_info["updated_time"]))


def decode_jwt_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, JWT_KEY, algorithms=['HS256'])
    except JWTClaimsError as e:
        return None
    except ExpiredSignatureError as e:
        return None
    except JWTError as e:
        return None
