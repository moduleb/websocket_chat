import logging
from typing import Annotated

from sqlalchemy import except_

from app.db.schemas.user import UssrDTO
from app.services.servise_factory import ServiceFactory, get_service_factory
from app.services.sessions.init import cookie
from fastapi import APIRouter, Depends, HTTPException, Response, status
from app.services.sessions.verifier import verifier
from app.db.schemas.session import SessionData
from app.services.user_service import UserNotFoundError, WrongPasswordError

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/", dependencies=[Depends(cookie)])
async def profile(
    user_dto: UssrDTO,
    response: Response,
    service_factory: Annotated[ServiceFactory, Depends(get_service_factory)],
    session_data: Annotated[SessionData, Depends(verifier)],
):
    """Авторизация, сохраняет сессию в cookie."""
    user_service = service_factory.get_user_service()
    session_service = service_factory.get_session_service()

    if session_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь уже авторизован.",
        )

    try:
        user = await user_service.get_user(user_dto)

    except (WrongPasswordError, UserNotFoundError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль.",
        )

    session = await session_service.create(user.id)
    cookie.attach_to_response(response, session)
    return {"message": "Successfully logged in"}
