from bson import ObjectId
from pymongo import ReturnDocument
from backend.database import database

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

    return vehicle
