
from pydantic import BaseModel


class SessionData(BaseModel):
    """Модель данных сессии."""

    username: str
