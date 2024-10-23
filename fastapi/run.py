
from contextlib import asynccontextmanager

import uvicorn
from app.api import login, logout, messages, register, users, ws
from app.settings import settings
from app.utils.exception_handler import http_exception_handler
from app.utils.start_app_helpers import (
    check_db_connection,
    connect_to_redis,
    disconnect_redis,
)
from app.views import chat, index, success
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await connect_to_redis()
        await check_db_connection()
        yield
    except RuntimeError as e:
        raise SystemExit(str(e)) from e
    finally:
        await disconnect_redis()


app = FastAPI(title="ICQ 2024", lifespan=lifespan)


# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Api Endpoints
app.include_router(ws.router)
app.include_router(login.router, prefix="/api/login", tags=["API Endpoints"])
app.include_router(logout.router, prefix="/api/logout", tags=["API Endpoints"])
app.include_router(register.router, prefix="/api/register", tags=["API Endpoints"])
app.include_router(users.router, prefix="/api/users", tags=["API Endpoints"])
app.include_router(messages.router, prefix="/api/messages", tags=["API Endpoints"])

# Pages
app.include_router(index.router, prefix="", tags=["Pages"])
app.include_router(chat.router, prefix="/chat", tags=["Pages"])
app.include_router(success.router, prefix="/success", include_in_schema=False)

# Подключаем статические файлы
app.mount("/static", StaticFiles(directory="static"), name="static")


# Обработка ошибок
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return await http_exception_handler(request, exc)


# Обработчик для несуществующих маршрутов
@app.get("/{full_path:path}", response_class=HTMLResponse)
async def catch_all(full_path: str):
    """Вызывает исключение при переходе на незарегистрированным маршрутам.
    Далее exception_handler (функция выше) обработает это исключение.
    Без явного вызова исключения, обработать его не получится.
    """
    raise HTTPException(404)


if __name__ == "__main__":
    uvicorn.run(app, log_level=settings.LOG_LEVEL.lower())
