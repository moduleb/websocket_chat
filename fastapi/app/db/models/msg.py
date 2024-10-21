from sqlalchemy import Column, String, DateTime, Integer
from .user import Base
from datetime import datetime


class Msg(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, index=True)
    to = Column(String, nullable=False)
    from_ = Column(String, nullable=False)  # Используйте from_ вместо from
    text = Column(String, nullable=False)
    datetime = Column(DateTime, default=datetime.utcnow)  # Устанавливаем текущее время по умолчанию
