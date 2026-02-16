from beanie import Document, PydanticObjectId
from datetime import datetime
from typing import Optional

class Event(Document):
    title:str
    description: str
    location: str
    date: datetime
    price: float
    total_seats: int
    available_seats: int
    organizer_id:PydanticObjectId # links to the organizer's user model
    status: str = "draft" # defaul status

    ## how are we gonna make sure they cahnge from draft to publish to cancelled?

    class Settings:
        name="events"