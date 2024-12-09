from pydantic import BaseModel, Field

from backend.models.object_id import PyObjectId
from enum import Enum
from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional


class TokenTypeEnum(str, Enum):
    ACCESS = 'access'
    RESETPASSWORD = 'reset-password'
    DUMMY = 'dummy'


class Token(BaseModel):
    id: PyObjectId = Field(alias='_id')
    type: TokenTypeEnum
    user_id: Optional[str] = None
    token: str

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True


class AllToken(BaseModel):
    total: int
    page: int
    data: list[Token]
