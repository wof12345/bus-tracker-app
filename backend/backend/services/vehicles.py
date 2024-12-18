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


def get_vehicles(skip=0, limit=100000, reservation_id=None, route_id=None):
    query = {}
    if reservation_id:
        query['reservation._id'] = ObjectId(reservation_id)

    if route_id:
        query['route._id'] = ObjectId(route_id)

    # vehicles = list(collection.find(query).skip(skip).limit(limit))

    # vehicles = populate_array_ref(vehicles, 'users', 'driver')
    # vehicles = populate_array_ref(vehicles, 'users', 'helper')
    # vehicles = populate_array_ref(vehicles, 'routes', 'route')
    # vehicles = populate_array_ref(vehicles, 'reservations', 'reservation')

    pipeline = [
        {'$match': query},
        {'$skip': skip},
        {'$limit': limit},
        {
            '$lookup': {
                'from': 'users',
                'localField': 'driver._id',
                'foreignField': '_id',
                'as': 'driver',
            }
        },
        {
            '$lookup': {
                'from': 'users',
                'localField': 'helper._id',
                'foreignField': '_id',
                'as': 'helper',
            }
        },
        {
            '$lookup': {
                'from': 'routes',
                'localField': 'route._id',
                'foreignField': '_id',
                'as': 'route',
            }
        },
        {
            '$lookup': {
                'from': 'reservations',
                'localField': 'reservation._id',
                'foreignField': '_id',
                'as': 'reservation',
            }
        },
        {'$unwind': {'path': '$driver', 'preserveNullAndEmptyArrays': True}},
        {'$unwind': {'path': '$helper', 'preserveNullAndEmptyArrays': True}},
        {'$unwind': {'path': '$route', 'preserveNullAndEmptyArrays': True}},
        {'$unwind': {'path': '$reservation', 'preserveNullAndEmptyArrays': True}},
    ]

    vehicles = list(collection.aggregate(pipeline))

    return vehicles


def get_vehicle(filters):
    pipeline = [
        {'$match': filters},
        {
            '$lookup': {
                'from': 'users',
                'localField': 'driver._id',
                'foreignField': '_id',
                'as': 'driver',
            }
        },
        {
            '$lookup': {
                'from': 'users',
                'localField': 'helper._id',
                'foreignField': '_id',
                'as': 'helper',
            }
        },
        {
            '$lookup': {
                'from': 'routes',
                'localField': 'route._id',
                'foreignField': '_id',
                'as': 'route',
            }
        },
        {
            '$lookup': {
                'from': 'reservations',
                'localField': 'reservation._id',
                'foreignField': '_id',
                'as': 'reservation',
            }
        },
        {'$unwind': {'path': '$driver', 'preserveNullAndEmptyArrays': True}},
        {'$unwind': {'path': '$helper', 'preserveNullAndEmptyArrays': True}},
        {'$unwind': {'path': '$route', 'preserveNullAndEmptyArrays': True}},
        {'$unwind': {'path': '$reservation', 'preserveNullAndEmptyArrays': True}},
        {'$limit': 1},
    ]

    result = list(collection.aggregate(pipeline))

    return result[0] if result else None
