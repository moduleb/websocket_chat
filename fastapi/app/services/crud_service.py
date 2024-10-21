import logging
from typing import TypeVar

from app.db.models.user import Base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

logger = logging.getLogger(__name__)


# Определяем тип переменной для модели
ModelGeneric = TypeVar("ModelGeneric", bound=Base)


class CrudService:
    def __init__(self, session: AsyncSession, model: type[ModelGeneric]):
        self.session = session
        self.model = model

# --------------------------------------------------------------------------------------

    async def create(self, obj: ModelGeneric) -> ModelGeneric:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)  # Обновляем объект, чтобы получить его ID
        logger.debug("Сохранен в бд объект: %s", obj)
        return obj

# --------------------------------------------------------------------------------------

    async def get_one_by_filters(self, **filters) -> ModelGeneric | None:
        # Начинаем строить запрос
        query = select(self.model)

        # Применяем фильтры
        for key, value in filters.items():
            if hasattr(self.model, key):
                query = query.where(getattr(self.model, key) == value)
            else:
                logger.debug(
                    "Invalid filter key: %s." "No such attribute in model: %s",
                    key,
                    value,
                )

        # Выполняем запрос
        result = await self.session.execute(query)
        result_tuple = result.first()
        result = result_tuple[0] if result_tuple else None
        logger.debug("Найдены объекты: %s", result)
        return result

# --------------------------------------------------------------------------------------

    async def get_all_scalsrs(self, attr: str) -> list[str] | None:

        if not hasattr(self.model, attr):
            logger.debug("No such attribute in model: %s", attr)
            return

        query = select(getattr(self.model, attr))

        # Выполняем запрос
        result = await self.session.execute(query)
        result = list(result.scalars())
        logger.debug("Получено атрибутов: %s.", len(result))
        return result

# --------------------------------------------------------------------------------------

    async def get_all_by_filters_strategy_or(self, **filters) -> list[ModelGeneric] | None:
        # Начинаем строить запрос
        query = select(self.model)

        # Список условий для фильтров
        conditions = []

        # Применяем фильтры
        for key, value in filters.items():
            if hasattr(self.model, key):
                conditions.append(getattr(self.model, key) == value)
            else:
                logger.debug(
                    "Invalid filter key: %s. No such attribute in model: %s",
                    key,
                    value,
                )

        # Если есть условия, добавляем их в запрос с помощью or_
        if conditions:
            query = query.where(or_(*conditions))

        # Выполняем запрос
        result = await self.session.execute(query)
        result = result.all()  # Получаем все строки в виде списка Row
        result = [row[0] for row in result]
        logger.debug("Получено объектов: %s.", len(result))
        return result
