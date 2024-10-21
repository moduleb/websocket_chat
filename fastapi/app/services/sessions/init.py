from uuid import UUID

from app.db.schemas.session import SessionData
from app.settings import settings
from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.frontends.implementations import CookieParameters, SessionCookie

from .ws_cookie import WSSessionCookie

cookie_params = CookieParameters()

# Uses UUID
cookie = SessionCookie(
    cookie_name="session_id",
    identifier="general_verifier",
    auto_error=True,
    secret_key=settings.SESSION_SECRET_KEY,
    cookie_params=cookie_params,
)

ws_cookie = WSSessionCookie(
    cookie_name="session_id",
    identifier="general_verifier",
    auto_error=False,
    secret_key=settings.SESSION_SECRET_KEY,
    cookie_params=cookie_params,
)
backend = InMemoryBackend[UUID, SessionData]()
