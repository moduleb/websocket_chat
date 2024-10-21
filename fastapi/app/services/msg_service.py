import logging
from typing import Tuple

from app.db.models.msg import Msg
from app.db.schemas.msg import MsgDTO
from app.services.crud_service import CrudService
from pydantic import ValidationError

logger = logging.getLogger(__name__)


class MsgServiceError(Exception):
    pass


class MsgService:
    def __init__(self, msg_crud) -> None:
        self._crud: CrudService = msg_crud

    async def save_to_db(self, msg_dto: MsgDTO) -> None:
        msg_db: Msg = self._convert_msg_dto_to_msg_db(msg_dto)
        # await self._crud.create(msg_db)
        return msg_db

    @staticmethod
    def _convert_msg_dto_to_msg_db(msg_dto: MsgDTO) -> Msg:
        """Конвертируем DTO модель в SQLALCHEMY модель."""
        return Msg(to=msg_dto.to, from_=msg_dto.from_, text=msg_dto.text)

    @staticmethod
    def create_msg_dto(data: dict) -> MsgDTO | None:
        """Валидация входящего сообщения и создание модели MsgDTO."""
        try:
            return MsgDTO(**data)

        except ValidationError as e:
            msg = f"Ошибка валидации входящего сообщения.\nError: {e}"
            logger.warning(msg)
            raise MsgServiceError(msg) from e
