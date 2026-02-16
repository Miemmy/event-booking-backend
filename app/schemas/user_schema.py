#so we want a blueprint for the different time we will need the user in our api situation
# when we want to create a new user, when an old user want's to access stuff

from pydantic import BaseModel, EmailStr, Field
from beanie import PydanticObjectId
from typing import Optional 

#using field class for better documentation and all

class UserCreate(BaseModel):
    username: str = Field(..., example="john_doe")
    email: EmailStr = Field(..., example="johndoe@example.com")
    password: str = Field(..., example="strongpassword123")
    role: str = Field(..., pattern="^(organizer|attendee)$",example="attendee")

class UserLogin(BaseModel):
    email: EmailStr = Field(..., example="johndoe@example.com")
    password: str = Field(..., example="strongpassword123")

class UserOut(BaseModel):
    id: PydanticObjectId = Field(..., alias="_id")
    username: str
    email: EmailStr
    role: str
    # this what we will see when we return user info so that we won't expose sensitive data like password

    class Config:
         populate_by_name = True
         from_attributes = True # config so that pydntic works well with beanie odm objects