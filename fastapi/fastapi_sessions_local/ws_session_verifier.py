"""Generic verification code."""
import logging
from abc import abstractmethod
from typing import Generic

from app.services.sessions.init import ws_cookie
from fastapi import HTTPException, WebSocket
from fastapi_sessions.backends.session_backend import (
    BackendError,
    SessionBackend,
    SessionModel,
)
from fastapi_sessions.frontends.session_frontend import ID, FrontendError


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
            # session_id: Union[ID, FrontendError] = \
            # request.state.session_ids[self.identifier]
            logging.debug(f"Вызван метод call у  {self.__class__.__name__}")

            session_id: ID | FrontendError = \
            ws_cookie(websocket_)

            # request.state.session_ids[self.identifier]

        except Exception:
            if self.auto_error:
                raise HTTPException(
                    status_code=500, detail="internal failure of session verification"
                )
            return BackendError(
                "failed to extract the {} session from state", self.identifier
            )

        if isinstance(session_id, FrontendError):
            if self.auto_error:
                raise self.auth_http_exception
            return

        print(session_id)

        print("Получаем сессион дата")

        session_data = await self.backend.read(session_id)
        print(f"session_data= {session_data}")
        if not session_data or not self.verify_session(session_data):
            print("Даты нет- ошибка!")
            if self.auto_error:
                raise self.auth_http_exception
            return

        return session_data
