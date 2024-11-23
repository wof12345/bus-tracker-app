import jwt
from fastapi import HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from backend.config import settings


class AuthenticateUser(HTTPBearer):
    def __init__(self):
        super().__init__()

    async def __call__(self, request: Request) -> Optional[dict]:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            token = credentials.credentials
            user_data = self.validate_token(token)
            request.state.user_id = user_data['sub']
            request.state.user_role = user_data['role']
            return user_data
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail='Invalid authorization'
            )

    def validate_token(self, token: str):
        payload = verify_token(token)
        if payload:
            if 'sub' in payload and 'role' in payload:
                user_role = payload['role']
                if user_role in ['admin', 'commuter', 'driver', 'helper', 'manager']:
                    return payload
                else:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail='Invalid role in token',
                    )
            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Token payload missing 'sub' or 'role'",
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail='Invalid token'
            )


def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Token expired')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Invalid token')


auth_scheme = AuthenticateUser()
