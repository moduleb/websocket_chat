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
    if not session_data:
        return
    user_id = session_data.user_id

    await websocket.accept()

    # connections[user_id] = websocket

    try:
        while True:
            await websocket.send_text(f"Welcome, {user_id}!")
            data = await websocket.receive_text()
            await websocket.send_text(str(data))

    except WebSocketDisconnect:
        del connections[user_id]

    except ValueError:
        pass
