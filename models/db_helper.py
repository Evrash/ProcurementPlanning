from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession, create_async_engine, async_sessionmaker, AsyncEngine)

from config import settings

class DatabaseHelper:
    def __init__(self, db_url: str) -> None:
        self.engine: AsyncEngine | None = create_async_engine(url=db_url)
        self.session_factory: async_sessionmaker[AsyncSession] | None = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False,
        )

    async def close(self) -> None:
        if self.engine is not None:
            await self.engine.dispose()
            self.engine = None
            self.session_factory = None

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        if self.session_factory is None:
            raise RuntimeError('Session factory not initialized')
        async with self.session_factory() as session:
            try:
                yield session
            except Exception as e:
                await session.rollback()
                raise
            finally:
                await session.close()

db_helper = DatabaseHelper(db_url=settings.DATABASE_URL)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async for session  in db_helper.session_getter():
        yield session
