import logging
from app.settings import settings
from celery import Celery

# Настройка Celery с использованием URL брокера
celery_app = Celery("main", broker=settings.REDIS_URL)


class TgService:
    def __init__(self) -> None:
        self.celery = celery_app

    def send_notification(self, to: int, from_: str):
        # Вызов задачи
        logging.debug(settings.REDIS_URL, self.celery)
        self.celery.send_task("main.send_notification", args=[to, from_])


tg_service = TgService()
