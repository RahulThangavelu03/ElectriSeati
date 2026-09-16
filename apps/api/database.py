from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@127.0.0.1:5433/electriseati"

engine = create_async_engine(DATABASE_URL)