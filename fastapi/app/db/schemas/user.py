import re
import string
from typing import Optional

from pydantic import BaseModel, Field 


class UssrDTO(BaseModel):
    telegram_id: int | None = Field(default=None, examples=[123456789])
    username: str = Field(min_length=3, pattern=r"^[a-zA-Z0-9_]+$", examples=["user"])
    password: str = Field(
        min_length=6,
        pattern=r"^[{}]+$".format(
            string.ascii_letters
            + string.digits
            + re.escape(string.punctuation)  # допустимые символы
        ),
        examples=["password"]
    )
    class Config:
        from_attributes = True

class UserLoginDTO(UssrDTO):
    telegram_id: int = Field(default=None, exclude=True)  # Исключаем поле 

    # @field_validator("password")
    # def validate_password(cls, v): 
    #     if not any(c.islower() for c in v):
    #         msg = "Password must contain at least one lowercase letter."
    #         raise ValueError(msg)
    #     if not any(c.isupper() for c in v):
    #         msg = "Password must contain at least one uppercase letter."
    #         raise ValueError(msg)
    #     if not any(c.isdigit() for c in v):
    #         msg = "Password must contain at least one digit."
    #         raise ValueError(msg)
    #     if not any(c in string.punctuation for c in v):
    #         msg = "Password must contain at least one special character."
    #         raise ValueError(msg)
    #     return v

# from pydantic_sqlalchemy import sqlalchemy_to_pydantic
# UserPydantic = sqlalchemy_to_pydantic(User)
