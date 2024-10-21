# from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api import chat, login, logout, profile, register, users, ws, temp
from app.settings import settings
from fastapi import WebSocket
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     """Проверяем подключение к бд. Закрываем приложение елси бд недоступна."""
#     if not await is_connected_to_db():
#         msg = "База данных недоступна, Выход..."
#         raise SystemExit(msg)
#     yield

# Настройка асинхронного Redis для хранения сессий
# redis_client = aioredis.from_url("redis://localhost")
# backend = RedisBackend(redis_client)

# app = FastAPI(title="IM CHAT", lifespan=lifespan)
app = FastAPI(title="IM CHAT")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Или укажите конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()  # Принять соединение
#     while True:
#         data = await websocket.receive_text()  # Получить текстовое сообщение
#         await websocket.send_text(f"Вы сказали: {data}")  # Отправить ответ

app.include_router(ws.router, tags=["Endpoints"])
app.include_router(login.router, prefix="/login", tags=["Endpoints"])
app.include_router(logout.router, prefix="/logout", tags=["Endpoints"])
app.include_router(register.router, prefix="/register", tags=["Endpoints"])
app.include_router(profile.router, prefix="/profile", tags=["Endpoints"])
app.include_router(users.router, prefix="/users", tags=["Endpoints"])
app.include_router(chat.router, prefix="/chat", tags=["Endpoints"])


# Подключаем статические файлы
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run(app, log_level=settings.LOG_LEVEL.lower())
