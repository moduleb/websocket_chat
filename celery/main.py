from celery import Celery

from settings import settings

import asyncio
import logging
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest

logger = logging.getLogger(__name__)


# Создаем экземпляр Celery
app = Celery("main", broker=settings.REDIS_URL,
             backend=settings.REDIS_URL)

# Установите параметр для повторных попыток подключения
app.conf.broker_connection_retry_on_startup = True

bot = Bot(settings.TOKEN)


@app.task
def send_notification(to: str, from_: str):
    msg = f"У вас есть новое сообщение от {from_}"

    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(bot.send_message(chat_id=to, text=msg))

    except TelegramBadRequest:
        logger.info(
            "Телеграм пользователя с таким id не существует, id: %s.", to)
    except Exception:
        logger.exception(
            "Ошибка при попытке отправки сообщения в телеграм "
            "пользователю id: %s.\n", to)
