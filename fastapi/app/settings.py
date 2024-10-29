import logging

from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings
from pydantic_settings.main import SettingsConfigDict


class Settings(BaseSettings):
    """Конфигурация приложения."""

    # Загружает переменные из файла .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # ----------------------------- Настройки Postgres --------------------------------
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    # Формирует строку подключения к бд
    @property
    def DATABASE_URL(self) -> PostgresDsn:
        dsn: PostgresDsn = (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
        return dsn

    # ------------------------------- Настройки Redis ----------------------------------
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    # Формирует строку подключения к Redis
    @property
    def REDIS_URL(self) -> RedisDsn:
        dsn: RedisDsn = f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return dsn

    # ------------------------------- Настройки Логера ---------------------------------
    LOG_LEVEL: str = "INFO"

    # ------------------------------- Секреты ------------------------------------------
    SESSION_SECRET_KEY: str


settings = Settings()

# Установка уровня логгирования
logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL))
