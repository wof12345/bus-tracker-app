from fastapi import APIRouter, HTTPException, Depends
from backend.schemas.auth import UserRegisterSchema, UserLoginSchema, TokenResponse
from backend.services.auth import register_user, login_user, verify_user
from backend.utils.auth_scheme import auth_scheme
from backend.models.user import UserResponse

router = APIRouter()


@router.post('/register/', response_model=dict)
def register(user: UserRegisterSchema):
    return register_user(user.email, user.password, user.role)


@router.post('/login/', response_model=TokenResponse)
def login(user: UserLoginSchema):
    return login_user(user.email, user.password, user.role)


@router.get('/verify', response_model=UserResponse)
def verify(user=Depends(auth_scheme)):
    return user
