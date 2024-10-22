import logging

from pydantic_settings import BaseSettings
from pydantic_settings.main import SettingsConfigDict


class Settings(BaseSettings):
    """Конфигурация приложения."""

    # Загружает переменные из файла .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # ------------------------------- Настройки Telegram -------------------------------
    TOKEN: str

    # ------------------------------- Настройки Логера ---------------------------------
    LOG_LEVEL: str = "INFO"

    APP_URL:str = "localhost"


settings = Settings()

# Установка уровня логгирования
logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL))
