from pydantic import BaseModel, Field
from typing import Optional
from backend.models.object_id import PyObjectId
from bson import ObjectId as BsonObjectId


class VehicleCreate(BaseModel):
    name: str
    license: str
    description: Optional[str] = None
    driver: str
    current_coordinates: str


class Vehicle(BaseModel):
    id: PyObjectId = Field(alias='_id')
    name: str
    license: str
    description: Optional[str] = None
    driver: str
    current_coordinates: str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {BsonObjectId: str}
