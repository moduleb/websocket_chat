import json
from typing import Generic

import redis.asyncio as aioredis
from app.db.schemas.session import SessionData
from app.settings import settings
from celery.utils.log import logging
from fastapi_sessions.backends.session_backend import (
    BackendError,
    SessionBackend,
    SessionModel,
)
from fastapi_sessions.frontends.session_frontend import ID

logger = logging.getLogger(__name__)


class RedisBackend(SessionBackend[ID, SessionModel], Generic[ID, SessionModel]):
    """Stores session data in Redis asynchronously."""

    def __init__(self) -> None:
        """Initialize a new Redis database."""
        self.redis_client = None

    async def _check_redis_connection(self):
        # Проверка подключения
        pong = await self.redis_client.ping()
        if pong:
            logger.debug("Успешно подключено к Redis")
        else:
            logger.error("Не удалось подключиться к Redis")

    async def connect(self):
        """Connect to the Redis database."""
        self.redis_client = await aioredis.from_url(settings.REDIS_URL)
        await self._check_redis_connection()

    async def close(self):
        """Close the Redis connection."""
        if self.redis_client:
            await self.redis_client.close()

    async def create(self, session_id: ID, data: SessionModel):
        """Create a new session entry."""
        if await self.redis_client.exists(str(session_id)):
            raise BackendError("create can't overwrite an existing session")

        await self.redis_client.set(str(session_id), data.model_dump_json())

    async def read(self, session_id: ID):
        """Read an existing session data."""
        data = await self.redis_client.get(str(session_id))
        if not data:
            return
        return SessionData(**json.loads(data))

    async def update(self, session_id: ID, data: SessionModel) -> None:
        """Update an existing session."""
        if await self.redis_client.exists(str(session_id)):
            await self.redis_client.set(str(session_id), data.model_dump_json())
        else:
            raise BackendError("session does not exist, cannot update")

    async def delete(self, session_id: ID) -> None:
        """Delete an existing session."""
        await self.redis_client.delete(str(session_id))
