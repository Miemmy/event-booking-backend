from beanie import Document, PydanticObjectId
from datetime import datetime

class Booking(Document):
    user_id: PydanticObjectId #we get that from user model
    event_id:PydanticObjectId # we get that from event model
    ticket_quantity:int=1
    status:str="confirmed"
    booked_at: datetime = datetime.utcnow()

    class Settings:
        name="bookings"

