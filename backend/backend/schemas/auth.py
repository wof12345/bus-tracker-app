from pydantic import BaseModel, EmailStr
from backend.models.user import RoleEnum


class UserRegisterSchema(BaseModel):
    email: EmailStr
    role: RoleEnum
    password: str


class UserLoginSchema(BaseModel):
    email: EmailStr = 'admin@example.com'
    role: RoleEnum = 'admin'
    password: str = '1234'


class UserResponseSchema(BaseModel):
    email: str
    is_verified: bool


class TokenResponse(BaseModel):
    token: str
    token_type: str
