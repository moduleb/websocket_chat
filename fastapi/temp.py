from celery import Celery
from app.settings import settings

# Настройка Celery с использованием URL брокера
celery_app = Celery('main', broker=settings.REDIS_URL)

# Вызов задачи
data = {
    "tg_id": "5312665858",  # ID чата в Telegram
    "from_": "Имя отправителя"
}

# Вызов задачи
celery_app.send_task('main.send_notification', args=[data])
