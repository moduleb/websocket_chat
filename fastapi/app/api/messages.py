import logging
from typing import Annotated

from app.db.schemas.msg import ApiResponse, MsgDTO, MsgHistory
from app.db.schemas.session import SessionData
from app.services.servise_factory import ServiceFactory, get_service_factory
from app.services.sessions.init import cookie
from app.services.sessions.verifier import verifier
from fastapi import APIRouter, Depends, status

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get(
    "/",
    dependencies=[Depends(cookie)],
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse,
)
async def messages(
    recipient: str,
    service_factory: Annotated[ServiceFactory, Depends(get_service_factory)],
    session_data: Annotated[SessionData, Depends(verifier)],
):
    """Возвращает историю сообщения двух пользователей."""
    msg_service = service_factory.get_msg_service()

    # Отправляем историю сообщений
    messages: list[MsgDTO] = await msg_service.get_all_mesages(
        recipient, session_data.username
    )

    return {"data": {"username": session_data.username, "messages": messages}}
