import logging
from typing import TYPE_CHECKING, Annotated

from app.db.schemas.user import UssrDTO
from app.services.servise_factory import ServiceFactory, get_service_factory
from app.services.sessions.init import cookie
from app.services.user_service import UserNotFoundError, WrongPasswordError
from fastapi import APIRouter, Depends, HTTPException, Response, status

if TYPE_CHECKING:
    from app.db.models.user import User

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/")
async def login(
    user_dto: UssrDTO,
    response: Response,
    service_factory: Annotated[ServiceFactory, Depends(get_service_factory)],
):
    """Авторизация, сохраняет сессию в cookie."""
    user_service = service_factory.get_user_service()
    session_service = service_factory.get_session_service()

    try:
        user: User = await user_service.verify_user(user_dto)

    except (WrongPasswordError, UserNotFoundError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль.",
        )

    session = await session_service.create(user.username)
    cookie.attach_to_response(response, session)
    return {"message": "Successfully logged in"}
