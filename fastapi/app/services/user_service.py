import logging
from app.db.models.user import User
from app.db.schemas.user import UssrDTO
from app.services.crud_service import CrudService
from app.utils.password_utils import hash_password, verify_password

logger = logging.getLogger(__name__)


class UserServiceError(Exception):
    """Базовая ошбика сервиса."""


class UserNotFoundError(UserServiceError):
    """Пльзователь не найден."""


class WrongPasswordError(UserServiceError):
    """Неверный пароль."""


class UserService:
    def __init__(self, crud_service: CrudService):
        self.crud = crud_service

    async def create_user(self, user_dto: UssrDTO) -> User:
        user = User(
            username=user_dto.username,
            password=hash_password(user_dto.password),
            telegram_id=user_dto.telegram_id,
        )
        return await self.crud.create(user)

    async def get_user(self, user_dto: UssrDTO) -> User | None:
        user = await self.crud.get_one_by_filters(username=user_dto.username)

        if not user:
            msg = f"Не найден пользователь с таким username: {user_dto.username}"
            logger.debug(msg)
            raise UserNotFoundError(msg)

        if not verify_password(
            plain_password=user_dto.password, hashed_password=user.password
        ):
            msg = "Неверный пароль"
            logger.debug(msg)
            raise WrongPasswordError(msg)

        return user

    async def get_user_by_id(self, user_id: int) -> User | Exception:
        user = await self.crud.get_one_by_filters(id=user_id)

        if not user:
            msg = f"Не найден пользователь с таким id: {user_id}"
            logger.debug(msg)
            raise UserNotFoundError(msg)

        return user
