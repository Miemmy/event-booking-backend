# okay so we using motor since beanie runs concurrently with it

import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

async def init_db():
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not set in the environment variables.")
    
    client= AsyncIOMotorClient(DATABASE_URL)

    from app.models.user import  User
    from app.models.events import Event
    from app.models.bookings import Booking

    await init_beanie(
        database= client.event_booking_db,
        document_models=[User, Event, Booking]
    )
    