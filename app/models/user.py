from beanie import Document
from pydantic import BaseModel, EmailStr
from typing import Optional

class User(Document):
    username: str
    email: EmailStr
    password_hash: str
    role:str


    class Settings:
        name = "users"

