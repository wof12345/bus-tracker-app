from fastapi import APIRouter, HTTPException, Path
from pymongo import ReturnDocument
from backend.models.routes import (
    Route,
    RouteCreate,
    RouteUpdate,
    AllRouteResponse,
)
from bson import ObjectId
from backend.database import database
from backend.utils.validate_object_id import validate_object_id
from backend.utils.pagination import get_pagination_data

router = APIRouter()

collection = database['routes']


# Helper function to validate ObjectId


@router.post('/', response_model=Route)
def create_route(item: RouteCreate):
    item_dict = item.model_dump(by_alias=True)

    result = collection.insert_one(item_dict)

    inserted_item = collection.find_one({'_id': result.inserted_id})

    if inserted_item:
        return inserted_item
    raise HTTPException(status_code=404, detail='Item not found after insertion')


@router.get('/', response_model=AllRouteResponse)
def get_all_routes(page: int = 1, per_page: int = 10):
    skip, limit = get_pagination_data(page, per_page)
    total = collection.count_documents({})
    routes = list(collection.find().skip(skip).limit(limit))

    return {
        'total': total,
        'page': page,
        'data': routes,
    }


@router.get('/{id}', response_model=Route)
def get_route_by_id(id: str = Path(..., title='Route ID')):
    validate_object_id(id)
    route = collection.find_one({'_id': ObjectId(id)})
    if route:
        return route
    raise HTTPException(status_code=404, detail='Route not found')


@router.put('/{id}', response_model=Route)
def update_route(
    id: str = Path(..., title='Route ID'),
    update_data: RouteUpdate = None,
):
    validate_object_id(id)
    update_data_dict = update_data.model_dump(exclude_unset=True, by_alias=True)
    updated_route = collection.find_one_and_update(
        {'_id': ObjectId(id)},
        {'$set': update_data_dict},
        return_document=ReturnDocument.AFTER,
    )
    if updated_route:
        return updated_route
    raise HTTPException(status_code=404, detail='Route not found')


@router.delete('/{id}')
def delete_route(id: str = Path(..., title='Route ID')):
    validate_object_id(id)
    result = collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count == 1:
        return {'message': 'Route deleted successfully'}
    raise HTTPException(status_code=404, detail='Route not found')
