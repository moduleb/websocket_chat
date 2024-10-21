import logging
from uuid import UUID, uuid4

from app.db.schemas.session import SessionData
from app.services.sessions.init import backend

logger = logging.getLogger(__name__)


class SessionServise:
    def __init__(self) -> None:
        self.backend = backend
        self.SessionData = SessionData

    async def create(self, username: str):
        session = uuid4()
        data = self.SessionData(username=username)
        await self.backend.create(session, data)
        logger.debug("Создана новая сессия для '%s'", username)
        return session

    async def delete(self, session_id: UUID):
        await self.backend.delete(session_id)


session_service = SessionServise()
