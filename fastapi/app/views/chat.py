import logging
from typing import TYPE_CHECKING, Annotated

from app.db.schemas.session import SessionData
from app.services.servise_factory import ServiceFactory, get_service_factory
from app.services.sessions.init import cookie
from app.services.sessions.verifier import verifier
from fastapi import APIRouter, Depends, Response, status, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

if TYPE_CHECKING:
    from app.db.models.user import User

router = APIRouter()

logger = logging.getLogger(__name__)

templates = Jinja2Templates(directory="templates")

@router.get("/", dependencies=[Depends(cookie)])
async def chat(
    request: Request,
    service_factory: Annotated[ServiceFactory, Depends(get_service_factory)],
    session_data: Annotated[SessionData, Depends(verifier)],
):
    user_service = service_factory.get_user_service()
    # username = session_data.username
    return templates.TemplateResponse("chat.html", {"request": request})
