from sqlalchemy.orm import Session

import schemas.user_schemas as schemas
import entity.user_entity as models
from util.user_util import hash_password


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def update_user_by_username(db: Session, username: str, user_update: schemas.UserUpdate):
    user: models.User = db.query(models.User).filter(models.User.username == username).first()
    if user is not None:
        if user_update.password:
            user.password = hash_password(user_update.password)

        if user_update.attend_data:
            user.attend_data = user_update.attend_data

        db.commit()
    return user


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, password=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_user_without_hash(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
