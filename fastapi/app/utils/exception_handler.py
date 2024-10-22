# error_handlers.py
from fastapi import Request, HTTPException
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 403:
        msg: str = "Доступ запрещен!"
        link: str = "/register"
        link_text: str = "Войти или зарегестрировться"

        # Возвращаем рендеринг шаблона с передачей объекта request
        return templates.TemplateResponse("error.html", {
            "request": request,
            "msg": msg,
            "link": link,
            "link_text": link_text
        }, status_code=403)

    # Для других статусов, возвращаем стандартный обработчик
    return await request.app.default_exception_handler(request, exc)
