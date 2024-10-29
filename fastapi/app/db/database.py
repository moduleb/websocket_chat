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


# Инициализируем фабрику сессий
AsyncSessionLocal: AsyncSession | None = None


# Создаем асинхронный движок и фабрику сессий
async def db_init():
    async_engine: AsyncEngine = create_async_engine(settings.DATABASE_URL, echo=False)
    logger.debug("Строка подключения к базе данных:\n%s", async_engine.url)
    asyncsessionlocal = async_sessionmaker(async_engine, expire_on_commit=False)
    # Проверяем подключение к бд
    async with asyncsessionlocal() as session:
        await session.execute(select(1))
    logger.info("Успешно подключено к Базе данных.")
    return asyncsessionlocal


async def get_session():
    try:
        async with AsyncSessionLocal() as session:
            yield session
    except OSError:
        logger.critical("База данных недоступна.")
        raise HTTPException(status_code=500, detail="База данных недоступна")
