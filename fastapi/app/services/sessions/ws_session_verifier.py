"""Generic verification code."""
from abc import abstractmethod
from typing import Generic

from fastapi import HTTPException, WebSocket
from fastapi_sessions.backends.session_backend import (
    BackendError,
    SessionBackend,
    SessionModel,
)
from fastapi_sessions.frontends.session_frontend import ID, FrontendError

from .init import ws_cookie


class WSSessionVerifier(Generic[ID, SessionModel]):
    @property
    @abstractmethod
    def identifier(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def backend(self) -> SessionBackend[ID, SessionModel]:
        raise NotImplementedError

    @property
    @abstractmethod
    def auto_error(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def auth_http_exception(self) -> HTTPException:
        raise NotImplementedError

    @abstractmethod
    def verify_session(self, model: SessionModel) -> bool:
        raise NotImplementedError

    async def __call__(self, websocket_: WebSocket):
        try:
            session_id: ID | FrontendError = \
            ws_cookie(websocket_)

        except Exception:
            if self.auto_error:
                # await websocket_.close(code=1008)
                pass

            return BackendError(
                "failed to extract the {} session from state", self.identifier
            )

        if isinstance(session_id, FrontendError):
            if self.auto_error:
                pass
                # await websocket_.close(code=1000)
            return

        session_data = await self.backend.read(session_id)

        if not session_data or not self.verify_session(session_data):

            if self.auto_error:
                pass
                # await websocket_.close(code=1000)
            return

        return session_data
