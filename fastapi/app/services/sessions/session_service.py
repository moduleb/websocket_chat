import logging
from uuid import UUID, uuid4

from app.db.schemas.session import SessionData
from app.services.sessions.init import backend

logger = logging.getLogger(__name__)


class SessionServise:
    def __init__(self) -> None:
        self.backend = backend
        self.SessionData = SessionData

    async def create(self, user_id: int):
        session = uuid4()
        data = self.SessionData(user_id=user_id)
        await self.backend.create(session, data)
        logger.debug("Создана сессия id: %s", session)
        return session

    async def delete(self, session_id: UUID):
        await self.backend.delete(session_id)



session_service = SessionServise()
