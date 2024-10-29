from app.services.sessions.init import backend


async def connect_to_redis():
    if not await backend.connect():
        msg = "Redis недоступен, выход..."
        raise RuntimeError(msg)


async def disconnect_redis():
    await backend.close()
