# now we write the routes for a user to book an event

from beanie import PydanticObjectId
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.bookings import Booking
from app.models.events import Event
from app.models.user import User
from app.utils.crud_dependecies import get_current_user

from app.schemas.bookings_schema import BookingOut

router= APIRouter(prefix="/booking", tags=["Bookings"])

@router.post("/{event_id}", response_model=BookingOut, status_code=status.HTTP_201_CREATED)
async def book_event(event_id:PydanticObjectId, 
                     current_user=Depends(get_current_user)):
    event = await Event.get(event_id)
    if not event:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                               detail="This event does not exist.")
    if event.date < datetime.now():
        raise HTTPException(400, "This event has already ended")
    # you can't be buyin ticket for past events nau 

    if event.status != "published":
        raise HTTPException(
            status_code=400, 
            detail="Tickets are not available for this event yet."
        ) 
    if event.available_seats <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                 detail="Sorry, tickets for this event are sold out !!")
     #we check for existing booking , because for some reason i just wwant to limit it to one booking per person
    existing_booking= await Booking.find_one({"user_id": current_user.id,
                                               "event_id": event.id})
    if existing_booking:
          raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                               detail="You have already booked this event.")
    #now unto the main thing innit

    #first we handle that racing condition thing by decresing available seats by one befor we totally run out
    query = Event.find_one(
    Event.id == event.id,
    Event.available_seats > 0
)

    update_result = await query.inc({Event.available_seats: -1})

    if update_result is None: # that is the query failed (0 seats) 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="Sorry, tickets for this event are sold out !!")
    new_booking= Booking(
         user_id=current_user.id,
         event_id=event.id,
         status="confirmed",

   )
    await new_booking.insert()

    event.available_seats -= 1

    await event.save()

    return new_booking


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_booking(booking_id:PydanticObjectId, 
                         current_user=Depends(get_current_user)):
    booking= await Booking.get(booking_id)
    if not booking:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                               detail="Booking not found.")
    if booking.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                 detail="You are not authorized to cancel this booking.")
    if booking.status == "cancelled":
        raise HTTPException(
            status_code=400, 
            detail="This booking is already cancelled"
        )
    
    booking.status = "cancelled"
    await booking.save() # since different status were specified let's use soft delete instead
      
    event= await Event.get(booking.event_id)
    if event:
          event.available_seats += 1
          await event.save()
    
    return {"message":"Booking cancelled successfully."}

@router.get("/", response_model=list[BookingOut])
async def get_my_bookings(current_user=Depends(get_current_user)):
    bookings= await Booking.find({"user_id": current_user.id}).to_list() #every booking where the user_id matches the one in our get current user method
    return bookings

      