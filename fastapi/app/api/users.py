import logging
from typing import TYPE_CHECKING, Annotated

from app.db.schemas.session import SessionData
from app.services.servise_factory import ServiceFactory, get_service_factory
from app.services.sessions.init import cookie
from app.services.sessions.verifier import verifier
from fastapi import APIRouter, Depends, Response, status

if TYPE_CHECKING:
    from app.db.models.user import User

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/", dependencies=[Depends(cookie)], status_code=status.HTTP_200_OK)
async def users(
    service_factory: Annotated[ServiceFactory, Depends(get_service_factory)],
    session_data: Annotated[SessionData, Depends(verifier)],
):
    """Возвращает спискок имен пользователей, кроме собственного."""
    user_service = service_factory.get_user_service()
    username = session_data.username
    usernames: list[str] = await user_service.get_all_usernames()
    # Удаляем совственный username
    usernames.remove(username)

    return {"data": {"usernames": usernames, "you": username}}
