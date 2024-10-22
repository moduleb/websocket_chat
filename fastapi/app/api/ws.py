import logging
from typing import TYPE_CHECKING, Annotated

from app.db.schemas.session import SessionData
from app.services.msg_service import MsgServiceError
from app.services.servise_factory import ServiceFactory, get_service_factory
from app.services.sessions.verifier import ws_verifier
from fastapi import (
    APIRouter,
    Depends,
    WebSocket,
    WebSocketDisconnect,
)

if TYPE_CHECKING:
    from app.db.models.user import User
    from app.db.schemas.msg import MsgDTO


logger = logging.getLogger(__name__)


router = APIRouter()

connections = {}


@router.websocket("/ws")
async def accept_websocket_connection(
    websocket: WebSocket,
    service_factory: Annotated[ServiceFactory, Depends(get_service_factory)],
    session_data: Annotated[SessionData, Depends(ws_verifier)],
):

    msg_service = service_factory.get_msg_service()
    user_service = service_factory.get_user_service()

    username = session_data.username
    logger.debug("Подключился user: %s", username)

    await websocket.accept()
    connections[username] = websocket

    try:
        while True:

            """
            Получаем json сообщения:
            {
            "to": "john_doe",
            "text": "Hello, this is a message!"
            }
            """

            data = await websocket.receive_json()

            # Добавляем отправителя
            data["from_"] = username

            try:
                # Валидируем сообщение и создаем объект MsgDTO
                msg_dto: MsgDTO = msg_service.create_msg_dto(data)
                # Сохраняем в бд
                await msg_service.save_to_db(msg_dto)
                logger.debug("Получено сообщение от: %s", msg_dto.from_)

            except MsgServiceError as e:
                logger.debug("Ошибка во время сохранения сообщения в бд\nError: %s", e)
                continue

            if msg_dto.to in connections:

                # Находим websocket адресата
                websocket_recipient: WebSocket = connections[msg_dto.to]
                logger.debug("Webcoket адресата: %s найден: %s", msg_dto.to, websocket)

                # Отправляем сообщение
                await websocket_recipient.send_json(msg_dto.model_dump())
                logger.debug("Сообщение отправлено to: %s", msg_dto.to)

            else:
                # Находим получателя в бд
                user_recipient: User = await user_service.get_by_username(msg_dto.to)
                logger.debug("Адресат сообщения оффлайн, username: %s", msg_dto.to)

                if user_recipient:

                    tg_service.send_notification(to = user_recipient.telegram_id,
                                  from_ = msg_dto.from_)
                else:
                    logger.warning("Пользователя с username: %s не найден.", msg_dto.to)

    except WebSocketDisconnect:
        if username in connections:
            del connections[username]

    except ValueError:
        pass
