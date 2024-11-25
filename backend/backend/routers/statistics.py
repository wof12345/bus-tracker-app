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
from backend.services.vehicles import get_vehicles

router = APIRouter()


@router.get('/buses-by-reservations')
def get_all_reservations():
    collection = database['vehicles']

    statistics = {}
    total = 0
    unreserved = 0

    vehicles = get_vehicles()

    for vehicle in vehicles:
        total += 1
        if vehicle['reservation'] is not None:
            reservation_name = vehicle['reservation']['name']

            if reservation_name not in statistics:
                statistics[reservation_name] = 1
            else:
                statistics[reservation_name] += 1

        else:
            unreserved += 0

    statistics['Total'] = total
    statistics['Unreserved'] = unreserved

    return statistics
