import logging
from typing import Annotated

from app.db.schemas.session import SessionData
from app.services.servise_factory import ServiceFactory, get_service_factory
from app.services.sessions.verifier import ws_verifier
from fastapi import (
    APIRouter,
    Depends,
    WebSocket,
    WebSocketDisconnect,
)

logger = logging.getLogger(__name__)


router = APIRouter()

connections = {}


@router.websocket("/")
async def accept_websocket_connection(
    websocket: WebSocket,
    service_factory: Annotated[ServiceFactory, Depends(get_service_factory)],
    session_data: Annotated[SessionData, Depends(ws_verifier)],
):

    username = session_data.username

    await websocket.accept()

    connections[username] = websocket

    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(str(data))

    except WebSocketDisconnect:
        if user_id in connections:
            del connections[username]

    except ValueError:
        pass
