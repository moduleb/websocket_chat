import logging
from typing import Annotated
from uuid import UUID

from fastapi.responses import RedirectResponse

from app.services.servise_factory import ServiceFactory, get_service_factory
from app.services.sessions.init import cookie
from fastapi import APIRouter, Depends, Response, status

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/", status_code=status.HTTP_200_OK)
async def logout(
    response: Response,
    service_factory: Annotated[ServiceFactory, Depends(get_service_factory)],
    session_id: UUID = Depends(cookie),
):
    """Выход из системы. Удаляет сессию из cookie."""
    session_service = service_factory.get_session_service()

    # if session_id:
    await session_service.delete(session_id)
    cookie.delete_from_response(response)
    return RedirectResponse(url="/", status_code=303)
    # return {"message": "Successfully logged out"}

    # raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    #                     detail="Пользователь не авторизован.")
