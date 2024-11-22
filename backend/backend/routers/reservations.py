from fastapi import APIRouter, HTTPException, Path
from pymongo import ReturnDocument
from backend.models.reservation import (
    Reservation,
    ReservationCreate,
    ReservationUpdate,
    AllReservationResponse,
)
from bson import ObjectId
from backend.database import database
from backend.utils.validate_object_id import validate_object_id
from backend.utils.pagination import get_pagination_data

router = APIRouter()

collection = database['reservations']


# Helper function to validate ObjectId


@router.post('/', response_model=Reservation)
def create_reservation(item: ReservationCreate):
    item_dict = item.model_dump(by_alias=True)

    result = collection.insert_one(item_dict)

    inserted_item = collection.find_one({'_id': result.inserted_id})

    if inserted_item:
        return inserted_item
    raise HTTPException(status_code=404, detail='Item not found after insertion')


@router.get('/', response_model=AllReservationResponse)
def get_all_reservations(page: int = 1, per_page: int = 10):
    skip, limit = get_pagination_data(page, per_page)
    total = collection.count_documents({})
    reservations = list(collection.find().skip(skip).limit(limit))

    return {
        'total': total,
        'page': page,
        'data': reservations,
    }


@router.get('/{id}', response_model=Reservation)
def get_reservation_by_id(id: str = Path(..., title='Reservation ID')):
    validate_object_id(id)
    reservation = collection.find_one({'_id': ObjectId(id)})
    if reservation:
        return reservation
    raise HTTPException(status_code=404, detail='Reservation not found')


@router.put('/{id}', response_model=Reservation)
def update_reservation(
    id: str = Path(..., title='Reservation ID'),
    update_data: ReservationUpdate = None,
):
    validate_object_id(id)
    update_data_dict = update_data.model_dump(exclude_unset=True, by_alias=True)
    updated_reservation = collection.find_one_and_update(
        {'_id': ObjectId(id)},
        {'$set': update_data_dict},
        return_document=ReturnDocument.AFTER,
    )
    if updated_reservation:
        return updated_reservation
    raise HTTPException(status_code=404, detail='Reservation not found')


@router.delete('/{id}')
def delete_reservation(id: str = Path(..., title='Reservation ID')):
    validate_object_id(id)
    result = collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count == 1:
        return {'message': 'Reservation deleted successfully'}
    raise HTTPException(status_code=404, detail='Reservation not found')
