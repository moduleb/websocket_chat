from celery.utils.log import logging
from app.settings import settings
from celery import Celery

logger = logging.getLogger(__name__)


# Настройка Celery с использованием URL брокера
celery_app = Celery("main", broker=settings.REDIS_URL)


class TgService:
    def __init__(self) -> None:
        self.celery = celery_app

    def send_notification(self, to: int, from_: str):
        if to:
            self.celery.send_task("main.send_notification", args=[to, from_])
        else:
            logger.debug("Telegram ID не указан, pass...")


tg_service = TgService()
