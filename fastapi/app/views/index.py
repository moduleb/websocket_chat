import logging

from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()

logger = logging.getLogger(__name__)

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    msg: str = "Добро пожаловать!"
    link: str = "/static/register/index.html"
    link_text: str = "Войти или зарегистрировться"

    # Возвращаем рендеринг шаблона с передачей объекта request
    return templates.TemplateResponse("message.html", {
        "request": request,  # Передаем request для работы с URL и сессиями
        "msg": msg,
        "link": link,
        "link_text": link_text
    })
