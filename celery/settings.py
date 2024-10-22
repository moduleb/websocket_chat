import logging

from pydantic_settings import BaseSettings
from pydantic_settings.main import SettingsConfigDict


class Settings(BaseSettings):
    """Конфигурация приложения."""

    # Загружает переменные из файла .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # ------------------------------- Настройки Telegram -------------------------------
    TOKEN: str

    # ------------------------------- Настройки Redis ----------------------------------
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    # Формирует строку подключения к Redis
    @property
    def REDIS_URL(self):
        return f"redis://{self.REDIS_HOST}/0"

    # ------------------------------- Настройки Логера ---------------------------------
    LOG_LEVEL: str = "INFO"


settings = Settings()

# Установка уровня логгирования
logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL))
