from pydantic import BaseModel, Field
from typing import Optional
from backend.models.object_id import PyObjectId
from bson import ObjectId as BsonObjectId
from backend.models.hotspot import Hotspot


class RouteCreate(BaseModel):
    name: str
    description: Optional[str] = None
    coordinates: list[list[float]]
    lines: list[list[float]]
    hotspots: list[Hotspot]


class RouteUpdate(BaseModel):
    name: str
    description: Optional[str] = None
    lines: list[list[float]]
    coordinates: list[list[float]]
    hotspots: list[Hotspot]


class Route(BaseModel):
    id: PyObjectId = Field(alias='_id')
    name: str
    description: Optional[str] = None
    lines: list[list[float]]
    coordinates: list[list[float]]
    hotspots: list[Hotspot]

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {BsonObjectId: str}


class AllRouteResponse(BaseModel):
    total: int
    page: int
    data: list[Route]
