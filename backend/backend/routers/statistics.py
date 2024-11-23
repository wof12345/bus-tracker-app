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


@router.get('/buses_by_reservations')
def get_all_reservations():
    collection = database['vehicle']

    statistics = {}

    vehicles = list(collection.find())

    print(vehicles)

    return {
        'data': vehicles,
    }
