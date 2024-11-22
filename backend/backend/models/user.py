from pydantic import BaseModel, Field

from backend.models.object_id import PyObjectId
from enum import Enum
from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional


class RoleEnum(str, Enum):
    ADMIN = 'admin'
    COMMUTER = 'commuter'
    DRIVER = 'driver'
    HELPER = 'helper'
    MANAGER = 'manager'


class UserCreate(BaseModel):
    email: str
    password: str
    phone: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    address: Optional[str] = None
    role: RoleEnum
    is_verified: Optional[bool] = False


class UserUpdate(BaseModel):
    email: str
    phone: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    address: Optional[str] = None
    role: RoleEnum
    is_verified: Optional[bool] = False


class User(BaseModel):
    id: PyObjectId = Field(alias='_id')
    email: str
    password: str
    phone: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    address: Optional[str] = None
    role: RoleEnum
    is_verified: Optional[bool] = False

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True


class UserResponse(BaseModel):
    id: PyObjectId = Field(alias='_id')
    email: str
    role: RoleEnum
    phone: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    address: Optional[str] = None
    is_verified: bool = False

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True


class AllUserResponse(BaseModel):
    total: int
    page: int
    data: list[User]
