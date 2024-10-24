# error_handlers.py
from celery.utils.log import logging
from fastapi import Request, HTTPException
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

logger = logging.getLogger(__name__)


async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 403:
        msg: str = "Доступ запрещен!"
        link: str = "/static/register/index.html"
        link_text: str = "Войти или зарегестрировться"

    elif exc.status_code == 404:
        msg: str = "Страница не найдена"
        link: str = "/"
        link_text: str = "Перейти на главную"

    elif exc.status_code == 409:
        msg: str = "Страница не найдена"
        link: str = "/"
        link_text: str = "Перейти на главную"

    else:
        msg: str = "Неизвестная ошибка!"
        link: str = "/"
        link_text: str = "Перейти на главную"
        logger.exception("Неизвестная ошибка")

    return templates.TemplateResponse(
        "message.html",
        {"request": request, "msg": msg, "link": link, "link_text": link_text},
        status_code=exc.status_code,
    )
