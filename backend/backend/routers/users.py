from fastapi import APIRouter, HTTPException, Path
from pymongo import ReturnDocument
from backend.models.user import (
    User,
    UserCreate,
    UserUpdate,
    AllUserResponse,
    UserResponse,
)
from bson import ObjectId
from backend.database import database
from backend.utils.validate_object_id import validate_object_id
from backend.utils.pagination import get_pagination_data
from typing import Optional

router = APIRouter()

collection = database['users']


# Helper function to validate ObjectId


@router.post('/', response_model=User)
def create_user(item: UserCreate):
    item_dict = item.model_dump(by_alias=True)

    result = collection.insert_one(item_dict)

    inserted_item = collection.find_one({'_id': result.inserted_id})

    if inserted_item:
        return inserted_item
    raise HTTPException(status_code=404, detail='Item not found after insertion')


@router.get('/', response_model=AllUserResponse)
def get_all_users(role: Optional[str] = None, page: int = 1, per_page: int = 10):
    skip, limit = get_pagination_data(page, per_page)

    total = collection.count_documents({})

    query = {'role': role} if role else {}

    total = collection.count_documents(query)

    users = list(collection.find(query).skip(skip).limit(limit))

    return {
        'total': total,
        'page': page,
        'data': users,
    }


@router.get('/{id}', response_model=User)
def get_user_by_id(id: str = Path(..., title='User ID')):
    validate_object_id(id)
    user = collection.find_one({'_id': ObjectId(id)})
    if user:
        return user
    raise HTTPException(status_code=404, detail='User not found')


@router.put('/{id}', response_model=UserResponse)
def update_user(
    id: str = Path(..., title='User ID'),
    update_data: UserUpdate = None,
):
    validate_object_id(id)
    update_data_dict = update_data.model_dump(exclude_unset=True, by_alias=True)
    updated_user = collection.find_one_and_update(
        {'_id': ObjectId(id)},
        {'$set': update_data_dict},
        return_document=ReturnDocument.AFTER,
    )
    if updated_user:
        return updated_user
    raise HTTPException(status_code=404, detail='User not found')


@router.delete('/{id}')
def delete_user(id: str = Path(..., title='User ID')):
    validate_object_id(id)
    result = collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count == 1:
        return {'message': 'User deleted successfully'}
    raise HTTPException(status_code=404, detail='User not found')
