from fastapi import APIRouter, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from typing import List
from pymongo import ReturnDocument
from backend.models.hotspot import (
    Hotspot,
    HotspotCreate,
    HotspotUpdate,
    AllHotspotResponse,
)
from bson import ObjectId
from backend.database import database
from backend.utils.validate_object_id import validate_object_id
from backend.utils.pagination import get_pagination_data

router = APIRouter()

collection = database['hotspots']


# Helper function to validate ObjectId


@router.post('/', response_model=Hotspot)
def create_hotspot(item: HotspotCreate):
    item_dict = item.model_dump(by_alias=True)

    result = collection.insert_one(item_dict)

    inserted_item = collection.find_one({'_id': result.inserted_id})

    if inserted_item:
        return inserted_item
    raise HTTPException(status_code=404, detail='Item not found after insertion')


@router.get('/', response_model=AllHotspotResponse)
def get_all_hotspots(page: int = 1, per_page: int = 10):
    skip, limit = get_pagination_data(page, per_page)
    total = collection.count_documents({})
    hotspots = list(collection.find().skip(skip).limit(limit))

    return {
        'total': total,
        'page': page,
        'data': hotspots,
    }


@router.get('/{id}', response_model=Hotspot)
def get_hotspot_by_id(id: str = Path(..., title='Hotspot ID')):
    validate_object_id(id)
    hotspot = collection.find_one({'_id': ObjectId(id)})
    if hotspot:
        return hotspot
    raise HTTPException(status_code=404, detail='Hotspot not found')


@router.put('/{id}', response_model=Hotspot)
def update_hotspot(
    id: str = Path(..., title='Hotspot ID'),
    update_data: HotspotUpdate = None,
):
    validate_object_id(id)
    update_data_dict = update_data.model_dump(exclude_unset=True, by_alias=True)
    updated_hotspot = collection.find_one_and_update(
        {'_id': ObjectId(id)},
        {'$set': update_data_dict},
        return_document=ReturnDocument.AFTER,
    )
    if updated_hotspot:
        return updated_hotspot
    raise HTTPException(status_code=404, detail='Hotspot not found')


@router.delete('/{id}')
def delete_hotspot(id: str = Path(..., title='Hotspot ID')):
    validate_object_id(id)
    result = collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count == 1:
        return {'detail': 'Hotspot deleted successfully'}
    raise HTTPException(status_code=404, detail='Hotspot not found')
