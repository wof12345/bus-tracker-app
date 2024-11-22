from pydantic import BaseModel, Field
from typing import Optional
from backend.models.object_id import PyObjectId
from bson import ObjectId as BsonObjectId


class ReservationCreate(BaseModel):
    name: str
    description: Optional[str] = None


class ReservationUpdate(BaseModel):
    name: str
    description: Optional[str] = None


class Reservation(BaseModel):
    id: PyObjectId = Field(alias='_id')
    name: str
    description: Optional[str] = None

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {BsonObjectId: str}


class AllReservationResponse(BaseModel):
    total: int
    page: int
    data: list[Reservation]
