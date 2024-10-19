# from contextlib import asynccontextmanager
import uvicorn
from app.api import login, profile, register, ws, logout
from app.settings import settings
from fastapi import FastAPI

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

app.include_router(ws.router, prefix="/ws", tags=["Endpoints"])
app.include_router(login.router, prefix="/login", tags=["Endpoints"])
app.include_router(logout.router, prefix="/logout", tags=["Endpoints"])
app.include_router(register.router, prefix="/register", tags=["Endpoints"])
app.include_router(profile.router, prefix="/profile", tags=["Endpoints"])


if __name__ == "__main__":
    uvicorn.run(app, log_level=settings.LOG_LEVEL.lower())
