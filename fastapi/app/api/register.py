import logging
import re
from typing import Annotated

from app.db.schemas.user import UssrDTO
from app.services.servise_factory import ServiceFactory, get_service_factory
from app.services.sessions.init import cookie
from fastapi import APIRouter, Depends, HTTPException, Response, status, Request
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import UniqueViolationError


router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def register(
    user_dto: UssrDTO,
    # request: Request,
    service_factory: Annotated[ServiceFactory, Depends(get_service_factory)],
    response: Response,
):
    # request = await request.json()
    # print(request)
    # user = UssrDTO(**request)
    # return
    """Регистрация нового пользователя."""
    user_service = service_factory.get_user_service()
    session_service = service_factory.get_session_service()

    try:
        user = await user_service.create_user(user_dto)

    except IntegrityError as e:
        # Проверяем, является ли ошибка UniqueViolationError
        if "already exists" in str(e):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Username already exists.")

        logger.debug("Ошибка при регистрации пользователя.\nError: %s", e)
        raise HTTPException(status_code=500,
                            detail="Неизвестная ошибка, повторите попытку позднее...")

    except Exception as e:
        logger.debug("Ошибка при регистрации пользователя.\nError: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Неизвестная ошибка, повторите попытку позднее...",
        ) from e

    else:
        # Создаем сесссию
        session = await session_service.create(user.username)
        # Устанавливаем cookie
        cookie.attach_to_response(response, session)
        return {"message": "Successfully registered"}
