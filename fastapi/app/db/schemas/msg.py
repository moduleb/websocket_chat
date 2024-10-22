from datetime import datetime

from pydantic import BaseModel, Field


class MsgDTO(BaseModel):
    to: str = Field(min_length=3, pattern=r"^[a-zA-Z0-9_]+$", examples=["user"])
    from_: str = Field(min_length=3, pattern=r"^[a-zA-Z0-9_]+$", examples=["user"])
    text: str = Field(min_length=1, examples=["Hello from user!"])

    class Config:
        from_attributes = True


class MsgHistory(BaseModel):
    recipient: str = Field(min_length=3, pattern=r"^[a-zA-Z0-9_]+$", examples=["user1"])


# Определяем модель для ответа
class ResponseModel(BaseModel):
    username: str
    messages: list[MsgDTO]

# Определяем модель для общего ответа
class ApiResponse(BaseModel):
    data: ResponseModel
