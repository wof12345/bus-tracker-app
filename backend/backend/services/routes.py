from bson import ObjectId
from pymongo import ReturnDocument
from backend.database import database
from backend.utils.db_util import (
    populate_ref_array,
    populate_ref,
    populate_single_ref_array,
)


collection = database['routes']


def get_route(filters):
    route = collection.find_one(filters)

    route = populate_single_ref_array(route, 'hotspots', 'hotspots')

    return route
