from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from jose import jwt, JWTError
from typing import Optional
from datetime import datetime
from typing import List
from backend.models.user import RoleEnum
import jwt
from backend.config import settings
from backend.utils.auth_scheme import auth_scheme


ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


ALGORITHM = 'HS256'


async def get_current_user(payload: str = Depends(auth_scheme)):
    if not payload:
        raise HTTPException(status_code=401, detail='Could not validate credentials')
    return payload


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user):
    payload = {
        'sub': user['email'],
        'role': user['role'],
        'exp': datetime.utcnow() + timedelta(days=3),
        'id': user['email'],
    }
    token = jwt.encode(payload, settings.jwt_secret, algorithm='HS256')
    return token


def role_required(allowed_roles: List[RoleEnum]):
    async def role_dependency(payload: dict = Depends(get_current_user)):
        print(payload)
        user_role = payload.get('role')
        if user_role not in [role.value for role in allowed_roles]:
            raise HTTPException(status_code=403, detail='Permission denied')
        return payload

    return role_dependency
