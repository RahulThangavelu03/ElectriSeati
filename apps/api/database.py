from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@127.0.0.1:5433/electriseati"


class Base(DeclarativeBase):
    pass


engine = create_async_engine(DATABASE_URL)