from sqlalchemy import String, Column, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from .user import Base


class Msg(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    to: Mapped[str] = mapped_column(String(30))
    from_: Mapped[str] = mapped_column(String(30))
    text: Mapped[str] = mapped_column(String(200))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now())

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id!r}, to={self.to!r}, from_={self.from_!r})"
