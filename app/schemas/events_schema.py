from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from beanie import PydanticObjectId


class EventBase(BaseModel):
    title:str=Field(...,min_length=3,example="Tech Conference 2024")
    description:str=Field(...,min_length=10,example="An exciting conference about the latest in tech.")
    location:str=Field(...,min_length=3,example="New York City")
    date:datetime=Field(...,example="2024-12-01T10:00:00Z")
    price:float=Field(...,ge=0,example=99.99)
    total_seats: int=Field(...,gt=0,example=100)
    status: Optional[str] = Field(None, pattern="^(draft|published)$", example="published")

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3)
    description: Optional[str] = Field(None, min_length=10)
    location: Optional[str] = None
    date: Optional[datetime] = None
    price: Optional[float] = Field(None, ge=0)

    status: Optional[str] = None

class EventFilter(BaseModel):
    limit:int=Field(20, gt=0, le=100)
    skip:int=Field(0, ge=0)
    search:Optional[str]= None
    location: Optional[str]= None


class EventOut(EventBase):
    id: PydanticObjectId = Field(..., alias="_id")
    organizer_id: PydanticObjectId
    available_seats: int
    status: str

    class Config:
        populate_by_name = True
        from_attributes = True


