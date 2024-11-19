from backend.database import database
from fastapi import APIRouter, HTTPException
from typing import Optional


router = APIRouter()

collection = database['users']


def get_user(email: str):
    user = collection.find_one({'email': email})

    if not user:
        raise HTTPException(status_code=400, detail='User does not exist')

    return user
