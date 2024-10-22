# from contextlib import asynccontextmanager
import uvicorn
from app.api import login, logout, register, users, ws, messages
from app.views import chat, profile, success, index
from app.settings import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi import HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.utils.exception_handler import http_exception_handler


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     """Проверяем подключение к бд. Закрываем приложение елси бд недоступна."""
#     if not await is_connected_to_db():
#         msg = "База данных недоступна, Выход..."
#         raise SystemExit(msg)
#     yield

# app = FastAPI(title="IM CHAT", lifespan=lifespan)
app = FastAPI(title="IM CHAT")

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
# app.include_router(profile.router, prefix="/profile", tags=["Pages"])
app.include_router(success.router, prefix="/success", include_in_schema=False)

# Подключаем статические файлы
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return await http_exception_handler(request, exc)

# Обработчик для несуществующих маршрутов
@app.get("/{full_path:path}", response_class=HTMLResponse)
async def catch_all(full_path: str):
    raise HTTPException(404)

if __name__ == "__main__":
    uvicorn.run(app, log_level=settings.LOG_LEVEL.lower())
