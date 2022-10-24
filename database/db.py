from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from config.config import COCKROACH_URL
from sqlalchemy.orm import declarative_base, DeclarativeMeta

engine = create_engine(COCKROACH_URL)

Base: DeclarativeMeta = declarative_base()

session_maker = sessionmaker(engine, expire_on_commit=False)


async def create_db_and_tables():
    with engine.begin() as conn:
        conn.run_callable(Base.metadata.create_all)


def get_session():
    print("session_maker")
    db = session_maker()
    try:
        print("session_maker yield")
        yield db
    finally:
        print("session_maker closed")
        db.close()
