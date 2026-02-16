from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Annotated, List
from beanie.operators import RegEx
from app.models.events import Event
from app.models.bookings import Booking
from app.models.user import User
from beanie import PydanticObjectId
from app.schemas.bookings_schema import BookingOut
from app.schemas.events_schema import EventCreate, EventOut, EventUpdate, EventFilter

from app.utils.crud_dependecies import get_current_user, require_organizer

router= APIRouter(prefix="/events", tags=["Events"])

@router.post("/", response_model=EventOut, status_code=status.HTTP_201_CREATED)
async def create_new_event(event: EventCreate, current_user= Depends(require_organizer)):
    new_event= Event(
        title= event.title,
        description= event.description,
        location= event.location,
        date= event.date,
        price= event.price,
        total_seats= event.total_seats,
        available_seats= event.total_seats,
        organizer_id= current_user.id,
        status=event.status if event.status else "draft"
    )

    await new_event.insert()
    return new_event

@router.get("/", response_model=List[EventOut])
async def get_all_events(
    filters:Annotated[EventFilter, Query()], current_user= Depends(get_current_user)):

    query= Event.find_all()

    if filters.location:
        query = query.find({
            "location": {
                "$regex": filters.location,
                "$options": "i" # 'i' = case-insensitive
            }
        })

  
    if filters.search:
        query = query.find({
            "title": {
                "$regex": filters.search,
                "$options": "i"
            }
        })
    events = await query.sort("-date").skip(filters.skip).limit(filters.limit).to_list()
    return events

        



    ...

@router.get("/{id}", response_model=EventOut)
async def get_event_by_id(id:str , current_user=Depends(get_current_user)):
    event=await Event.get(id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.patch("/{id}", response_model=EventOut)
async def update_event(id: str, event_update: EventUpdate, current_user= Depends(require_organizer)):
    event= await Event.get(id)
    if not event:
        raise HTTPException(status_code=404,details="Event not found")
    if event.organizer_id != current_user.id: 
        raise HTTPException(status_code=403, detail="You do not have permission to update this event")
    
    update_dict= event_update.model_dump(exclude_unset=True)

    await event.set(update_dict)
    return event

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(id:str, current_user=Depends(require_organizer)):
    event= await Event.get(id)
    if not event:
        raise HTTPException(status_code=404, details="Event Not Found")
    if event.organizer_id != current_user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to delete this event")
    await event.delete()
    return {"message": "Event deleted successfully"}


# total bookings under an event route
@router.get("/{event_id}/bookings", response_model=List[BookingOut])
async def get_event_bookings(
    event_id: PydanticObjectId,
    current_user: User = Depends(get_current_user)
):
   
    event = await Event.get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # security .....
    # only the organizer can see the guest list
    if event.organizer_id != current_user.id:
        raise HTTPException(
            status_code=403, 
            detail="You are not authorized to view bookings for this event"
        )

    
    bookings = await Booking.find(
        Booking.event_id == event.id
    ).to_list()

    return bookings