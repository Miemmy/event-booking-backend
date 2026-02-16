from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from beanie import PydanticObjectId

class BookingOut(BaseModel):
    id: PydanticObjectId =Field(...,serialization_alias="_id")
    user_id: PydanticObjectId
    event_id:PydanticObjectId 
    status:str
    booked_at: datetime = Field(default_factory=datetime.now)

    #since one booking =one ticket, no need for that attribute in the schema anyway

    class Config:
        populate_by_name = True
        from_attributes = True