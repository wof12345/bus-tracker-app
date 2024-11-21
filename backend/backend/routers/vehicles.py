from backend.database import database
from backend.utils.validate_object_id import validate_object_id
from backend.utils.pagination import get_pagination_data
from fastapi import APIRouter, HTTPException, Path
from backend.models.vehicle import (
    Vehicle,
    VehicleCreate,
    AllVehicleResponse,
    VehicleUpdate,
)
from bson import ObjectId
from pymongo import ReturnDocument

router = APIRouter()

collection = database['vehicles']


@router.post('/', response_model=Vehicle)
def create_vehicle(item: VehicleCreate):
    item_dict = item.model_dump(by_alias=True)

    result = collection.insert_one(item_dict)

    inserted_item = collection.find_one({'_id': result.inserted_id})

    if inserted_item:
        return inserted_item
    raise HTTPException(status_code=404, detail='Item not found after insertion')


@router.get('/', response_model=AllVehicleResponse)
def get_all_vehicles(page: int = 1, per_page: int = 10):
    skip, limit = get_pagination_data(page, per_page)
    total = collection.count_documents({})
    vehicles = list(collection.find().skip(skip).limit(limit))

    return {
        'total': total,
        'page': page,
        'data': vehicles,
    }


@router.get('/{id}', response_model=Vehicle)
def get_hotspot_by_id(id: str = Path(..., title='Vehicles ID')):
    validate_object_id(id)
    hotspot = collection.find_one({'_id': ObjectId(id)})
    if hotspot:
        return hotspot
    raise HTTPException(status_code=404, detail='Vehicles not found')


@router.put('/{id}', response_model=Vehicle)
def update_hotspot(
    id: str = Path(..., title='Vehicles ID'),
    update_data: VehicleUpdate = None,
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
    raise HTTPException(status_code=404, detail='Vehicles not found')


@router.delete('/{id}')
def delete_hotspot(id: str = Path(..., title='Vehicles ID')):
    validate_object_id(id)
    result = collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count == 1:
        return {'message': 'Vehicles deleted successfully'}
    raise HTTPException(status_code=404, detail='Vehicles not found')
