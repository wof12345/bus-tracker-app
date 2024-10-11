from backend.database import database
from fastapi import APIRouter, HTTPException
from typing import Optional
from backend.models.vehicle import Vehicle, VehicleCreate


router = APIRouter()

collection = database['vehicles']


@router.post('/', response_model=Vehicle)
def create_vehicle(item: VehicleCreate):
    item_dict = item.model_dump(by_alias=True)

    result = collection.insert_one(item_dict)

    inserted_item = collection.find_one({'_id': result.inserted_id})

    print(inserted_item)

    if inserted_item:
        return inserted_item
    raise HTTPException(status_code=404, detail='Item not found after insertion')
