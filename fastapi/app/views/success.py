import logging
from typing import TYPE_CHECKING, Annotated

from app.db.schemas.session import SessionData
from app.services.servise_factory import ServiceFactory, get_service_factory
from app.services.sessions.init import cookie
from app.services.sessions.verifier import verifier
from fastapi import APIRouter, Depends, Response, status
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

if TYPE_CHECKING:
    from app.db.models.user import User

router = APIRouter()

logger = logging.getLogger(__name__)

templates = Jinja2Templates(directory="templates")


@router.get("/{type_}", response_class=HTMLResponse)
async def success(request: Request, type_: str):

    match type_:
        case "register":
            msg: str = "Успешная регистрация!"
            link: str = "/chat/"
            link_text: str = "Перейти в чат"
        case "login":
            msg: str = "Вы успешно авторизовались!"
            link: str = "/chat/"
            link_text: str = "Перейти в чат"
        case _:
            msg: str = "Добро пожаловать!"
            link: str = "/static/register/index.html"
            link_text: str = "Войти или зарегистрироваться"


    # Возвращаем рендеринг шаблона с передачей объекта request
    return templates.TemplateResponse("message.html", {
        "request": request,  # Передаем request для работы с URL и сессиями
        "msg": msg,
        "link": link,
        "link_text": link_text
    })
