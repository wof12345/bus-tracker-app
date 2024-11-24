from bson import ObjectId
from pymongo import ReturnDocument
from backend.database import database
from backend.utils.db_util import (
    populate_ref_array,
    populate_ref,
    populate_single_ref_array,
    populate_array_ref,
)

collection = database['vehicles']


def update_vehicle(update_data, id):
    updated_vehicle = collection.find_one_and_update(
        {'_id': ObjectId(id)},
        {'$set': update_data},
        return_document=ReturnDocument.AFTER,
    )

    return updated_vehicle


def get_vehicle(filters):
    vehicle = collection.find_one(filters)

    vehicle = populate_ref(vehicle, 'users', 'driver')
    vehicle = populate_ref(vehicle, 'users', 'helper')
    vehicle = populate_ref(vehicle, 'routes', 'route')
    vehicle = populate_ref(vehicle, 'reservations', 'reservation')

    return vehicle
