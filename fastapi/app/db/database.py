import logging

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.settings import settings

logger = logging.getLogger(__name__)

# Создаем асинхронные движок и фабрику сессий
async_engine: AsyncEngine = create_async_engine(settings.DATABASE_URL, echo=False)
AsyncSessionLocal: AsyncSession = async_sessionmaker(
    async_engine, expire_on_commit=False
)

logger.debug("Строка подключения к базе данных:\n%s", async_engine.url)


async def get_session():
    try:
        async with AsyncSessionLocal() as session:
            yield session
    except OSError:
        logger.critical("База данных недоступна.")
        raise HTTPException(status_code=500, detail="База данных недоступна")


async def is_connected_to_db() -> bool | None:
    """Проверка подключения к базе данных."""
    async for session in get_session():
        result = await session.execute(select(1))

        if result.scalar() == 1:
            logger.info("Успешно подключено к базе даннх.")
            return True
