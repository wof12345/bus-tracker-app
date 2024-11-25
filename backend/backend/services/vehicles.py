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


def get_vehicles(skip=0, limit=100000, reservation=None):
    query = {}
    if reservation:
        query['reservation._id'] = ObjectId(reservation)

    vehicles = list(collection.find(query).skip(skip).limit(limit))

    vehicles = populate_array_ref(vehicles, 'users', 'driver')
    vehicles = populate_array_ref(vehicles, 'users', 'helper')
    vehicles = populate_array_ref(vehicles, 'routes', 'route')
    vehicles = populate_array_ref(vehicles, 'reservations', 'reservation')

    return vehicles


def get_vehicle(filters):
    vehicle = collection.find_one(filters)

    vehicle = populate_ref(vehicle, 'users', 'driver')
    vehicle = populate_ref(vehicle, 'users', 'helper')
    vehicle = populate_ref(vehicle, 'routes', 'route')
    vehicle = populate_ref(vehicle, 'reservations', 'reservation')

    return vehicle
