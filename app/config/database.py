from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from typing import AsyncGenerator

from .settings import get_settings

settings = get_settings()

DB_URL = settings.DATABASE_URL

engine = create_async_engine(DB_URL, echo=False, future=True)

AsyncSessionLocal = sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)


class Base(DeclarativeBase): ...


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
