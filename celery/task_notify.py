import asyncio
import logging



from aiogram import Bot


from settings import settings
from celery import Celery

logger = logging.getLogger(__name__)


bot = Bot(settings.TOKEN)

# Создаем экземпляр Celery
app = Celery("main", broker=settings.REDIS_URL)

@app.task(name="main.send_notification")
def send_notification(data: dict):
    chat_id = data.get("tg_id")
    from_ = data.get("from_")
    msg = f"У вас есть новое сообщение от {from_}"

    try:
        asyncio.create_task(bot.send_message(chat_id=chat_id, text=msg))
    except Exception:
        logger.exception(
            "Ошибка при попытке отправки сообщения в телеграм"
            "пользователю id: %s.\n", chat_id)
