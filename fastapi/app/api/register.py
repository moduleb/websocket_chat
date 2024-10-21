import logging
from typing import Annotated

from app.db.schemas.user import UssrDTO
from app.services.servise_factory import ServiceFactory, get_service_factory
from app.services.sessions.init import cookie
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def register(
    user_dto: UssrDTO,
    service_factory: Annotated[ServiceFactory, Depends(get_service_factory)],
    response: Response,
):
    """Регистрация нового пользователя."""
    user_service = service_factory.get_user_service()
    session_service = service_factory.get_session_service()

    try:
        user = await user_service.create_user(user_dto)

    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        ) from e

    else:
        # Создаем сесссию
        session = await session_service.create(user.username)
        # Устанавливаем cookie
        cookie.attach_to_response(response, session)
        return {"message": "Successfully registered"}
