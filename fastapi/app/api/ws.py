import logging
from typing import Annotated

from app.db.schemas.session import SessionData
from app.services.servise_factory import ServiceFactory, get_service_factory
from app.services.sessions.init import cookie
from app.services.sessions.verifier import verifier
from fastapi import APIRouter, Depends, HTTPException, WebSocket, status

logger = logging.getLogger(__name__)


router = APIRouter()

connections = []


@router.websocket("/", dependencies=[Depends(cookie)])
async def accept_websocket_connection(
    websocket: WebSocket,
    service_factory: Annotated[ServiceFactory, Depends(get_service_factory)],
    session_data: Annotated[SessionData, Depends(verifier)],
):
    if not session_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не авторизован.",
        )

    await websocket.accept()
    connections.append(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(str(data))

    except ValueError:
        pass
