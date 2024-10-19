
from pydantic import BaseModel


class SessionData(BaseModel):
    """Модель данных сессии."""

    user_id: int
