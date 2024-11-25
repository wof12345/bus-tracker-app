from fastapi import APIRouter, HTTPException, Depends
from backend.schemas.auth import UserRegisterSchema, UserLoginSchema, TokenResponse
from backend.services.auth import register_user, login_user, verify_user
from backend.utils.auth_scheme import auth_scheme
from backend.models.user import UserResponse
from backend.services.users import get_user

router = APIRouter()


@router.post('/register/', response_model=dict)
def register(user: UserRegisterSchema):
    return register_user(
        user.email, user.password, user.role, user.first_name, user.last_name
    )


@router.post('/login/', response_model=TokenResponse)
def login(user: UserLoginSchema):
    return login_user(user.email, user.password, user.role)


@router.get('/verify', response_model=UserResponse)
def verify(user=Depends(auth_scheme)):
    db_user = get_user(user['id'])
    return db_user
