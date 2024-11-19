from pydantic import BaseModel, Field

from backend.models.object_id import PyObjectId
from enum import Enum
from bson import ObjectId
from pydantic import BaseModel, Field


class RoleEnum(str, Enum):
    ADMIN = 'admin'
    TEACHER = 'teacher'
    STUDENT = 'student'


class User(BaseModel):
    id: PyObjectId = Field(alias='_id')
    email: str
    password: str
    role: RoleEnum
    is_verified: bool = False

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True


class UserResponse(BaseModel):
    id: PyObjectId = Field(alias='_id')
    email: str
    role: RoleEnum
    is_verified: bool = False

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True
