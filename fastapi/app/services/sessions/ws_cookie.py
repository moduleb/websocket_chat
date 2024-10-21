import logging
from uuid import UUID

from fastapi import HTTPException, Response, WebSocket
from fastapi.openapi.models import APIKey, APIKeyIn
from fastapi.security.base import SecurityBase
from fastapi_sessions.frontends.session_frontend import FrontendError, SessionFrontend
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from itsdangerous.exc import BadTimeSignature

logger = logging.getLogger(__name__)
from fastapi_sessions.frontends.implementations.cookie import CookieParameters


class WSSessionCookie(SecurityBase, SessionFrontend[UUID]):
    def __init__(
        self,
        *,
        cookie_name: str,
        identifier: str,
        secret_key: str,
        cookie_params: CookieParameters,
        scheme_name: str | None = None,
        auto_error: bool = False,
    ):
        self.model: APIKey = APIKey(
            **{"in": APIKeyIn.cookie},
            name=cookie_name,
        )
        self._identifier = identifier
        self.scheme_name = scheme_name or self.__class__.__name__
        self.auto_error = auto_error
        self.signer = URLSafeTimedSerializer(secret_key, salt=cookie_name)
        self.cookie_params = cookie_params.copy(deep=True)

    @property
    def identifier(self) -> str:
        return self._identifier

    def __call__(self, websocket_: WebSocket) -> UUID | FrontendError:
        # Get the signed session id from the session cookie
        signed_session_id = websocket_.cookies.get(self.model.name)

        if not signed_session_id:
            return FrontendError("No session cookie attached to request")

        # Verify and timestamp the signed session id
        try:
            session_id = UUID(
                self.signer.loads(
                    signed_session_id,
                    max_age=self.cookie_params.max_age,
                    return_timestamp=False,
                )
            )

        except (SignatureExpired, BadSignature, BadTimeSignature):
            return FrontendError("Session cookie has invalid signature")

        return session_id

    def delete_from_response(self) -> None:
        pass

    def attach_to_response(self) -> None:
        pass
