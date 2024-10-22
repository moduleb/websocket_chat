# from contextlib import asynccontextmanager
import uvicorn
from app.api import login, logout, register, users, ws, messages
from app.views import chat, profile
from app.settings import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

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
app.include_router(login.router, prefix="/login", tags=["API Endpoints"])
app.include_router(logout.router, prefix="/logout", tags=["API Endpoints"])
app.include_router(register.router, prefix="/register", tags=["API Endpoints"])
app.include_router(users.router, prefix="/users", tags=["API Endpoints"])
app.include_router(messages.router, prefix="/messages", tags=["API Endpoints"])

# Pages
app.include_router(chat.router, prefix="/chat", tags=["Pages"])
app.include_router(profile.router, prefix="/profile", tags=["Pages"])

# Подключаем статические файлы
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run(app, log_level=settings.LOG_LEVEL.lower())
