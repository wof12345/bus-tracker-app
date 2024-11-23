from pydantic import BaseModel, Field
from typing import Optional
from backend.models.object_id import PyObjectId
from bson import ObjectId as BsonObjectId
from backend.models.hotspot import Hotspot
from backend.models.user import User
from backend.models.reservation import Reservation
from backend.models.routes import Route


class VehicleCreate(BaseModel):
    name: str
    license: str
    description: Optional[str] = None
    driver: Optional[User] = None
    helper: Optional[User] = None
    reservation: Optional[Reservation] = None
    starting_point: Optional[Hotspot] = None
    route: Optional[Route] = None
    time: Optional[str] = None
    current_coordinates: Optional[list[Optional[float]]] = None


class VehicleUpdate(BaseModel):
    name: str
    license: str
    description: Optional[str] = None
    driver: Optional[User] = None
    helper: Optional[User] = None
    reservation: Optional[Reservation] = None
    starting_point: Optional[Hotspot] = None
    route: Optional[Route] = None
    time: Optional[str] = None
    current_coordinates: Optional[list[Optional[float]]] = None


class Vehicle(BaseModel):
    id: PyObjectId = Field(alias='_id')
    name: str
    license: str
    description: Optional[str] = None
    driver: Optional[User] = None
    helper: Optional[User] = None
    reservation: Optional[Reservation] = None
    starting_point: Optional[Hotspot] = None
    route: Optional[Route] = None
    time: Optional[str] = None
    current_coordinates: Optional[list[Optional[float]]] = None

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {BsonObjectId: str}


class AllVehicleResponse(BaseModel):
    total: int
    page: int
    data: list[Vehicle]
