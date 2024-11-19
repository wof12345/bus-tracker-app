from pydantic import BaseModel, Field
from typing import Optional
from backend.models.object_id import PyObjectId
from bson import ObjectId as BsonObjectId


class HotspotCreate(BaseModel):
    name: str
    description: Optional[str] = None
    location_name: str
    coordinates: list[float]


class HotspotUpdate(BaseModel):
    name: str
    description: Optional[str] = None
    location_name: str
    coordinates: list[float]


class Hotspot(BaseModel):
    id: PyObjectId = Field(alias='_id')
    name: str
    location_name: str
    description: Optional[str] = None
    coordinates: list[float]

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {BsonObjectId: str}


class AllHotspotResponse(BaseModel):
    total: int
    page: int
    data: list[Hotspot]
