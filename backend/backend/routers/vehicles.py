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
from backend.services.vehicles import update_vehicle
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
def get_vehicle_by_id(id: str = Path(..., title='Vehicles ID')):
    validate_object_id(id)
    vehicle = collection.find_one({'_id': ObjectId(id)})
    if vehicle:
        return vehicle
    raise HTTPException(status_code=404, detail='Vehicles not found')


@router.put('/{id}', response_model=Vehicle)
def update_vehicle_endpoint(
    id: str = Path(..., title='Vehicles ID'),
    update_data: VehicleUpdate = None,
):
    validate_object_id(id)
    update_data = update_data.model_dump(exclude_unset=True, by_alias=True)

    updated_vehicle = update_vehicle(update_data, id)

    if updated_vehicle:
        return updated_vehicle
    raise HTTPException(status_code=404, detail='Vehicles not found')


@router.delete('/{id}')
def delete_vehicle(id: str = Path(..., title='Vehicles ID')):
    validate_object_id(id)
    result = collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count == 1:
        return {'message': 'Vehicles deleted successfully'}
    raise HTTPException(status_code=404, detail='Vehicles not found')
