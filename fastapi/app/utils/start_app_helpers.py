from app.db.database import is_connected_to_db
from app.services.sessions.init import backend


async def check_db_connection():
    """Проверяем подключение к бд. Закрываем приложение елси бд недоступна."""
    if not await is_connected_to_db():
        msg = "База данных недоступна, выход..."
        raise RuntimeError(msg)


async def connect_to_redis():
    if not await backend.connect():
        msg = "Redis недоступен, выход..."
        raise RuntimeError(msg)

async def disconnect_redis():
    await backend.close()
