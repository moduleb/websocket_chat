import logging

import bcrypt

logger = logging.getLogger(__name__)


# Функция для хеширования пароля
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


# Функция для проверки пароля
def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except ValueError as e:
        logger.debug("Ошибка при дехешировании пароля.\nError: %s", e)
        return False
