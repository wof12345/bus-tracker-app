from fastapi import HTTPException, status
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
from backend.database import database
from backend.utils.auth import hash_password, verify_password, create_access_token
from backend.models.user import RoleEnum

collection = database['users']


def register_user(
    email: str,
    password: str,
    role: RoleEnum,
    first_name: str,
    last_name: str,
):
    try:
        hashed_password = hash_password(password)
        new_user = {
            'email': email,
            'password': hashed_password,
            'first_name': first_name,
            'last_name': last_name,
            'is_verified': False,
            'role': role,
        }
        collection.insert_one(new_user)
        return {'message': 'User registered successfully'}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail='Email already exists')


def login_user(email: str, password: str, role: RoleEnum):
    user = collection.find_one({'email': email})

    if (
        not user
        or not verify_password(password, user['password'])
        or not role == user['role']
    ):
        raise HTTPException(status_code=400, detail='Invalid credentials')

    token = create_access_token(user)
    return {'token': token, 'token_type': 'bearer'}


def verify_user(user_id: str):
    result = collection.update_one(
        {'_id': ObjectId(user_id)}, {'$set': {'is_verified': True}}
    )
    if result.modified_count == 1:
        return {'message': 'User verified successfully'}
    raise HTTPException(status_code=404, detail='User not found')
