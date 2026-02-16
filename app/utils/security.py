import os
from datetime import datetime, timedelta,timezone
from typing import Optional
import jwt
from passlib.context import CryptContext
from dotenv import load_dotenv  

#so  in this file we set up the mini functions we will need in our auth routes and all
SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 20
REFRESH_TOKEN_EXPIRE_DAYS = 7



#first we have our fuction to verify password for user log-in
pwd_context= CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password:str, hashed_password:str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

#then we have the function to actually hash passwords
def hash_password(password:str) -> str:
    return pwd_context.hash(password)

# now we have functions for our jwt tokens and all
def create_access_token(data: dict, expires_delta: Optional[timedelta]=None) -> str:
     to_encode= data.copy()

     if expires_delta:
         expire= datetime.now(timezone.utc) + expires_delta #the expiry duration anchored to the current time
     else:
         expire= datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
     to_encode.update({"exp":expire,"type":"refresh"})
     encoded_jwt= jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
     return encoded_jwt

     #oh yh we kep using all this timesone stuff so that we don't run into that error of our token already xpiring before it was issued 😭😭

def create_refresh_token(data:dict,expires_delta:Optional[timedelta]=None) -> str:
    to_encode= data.copy()

    if expires_delta:
        expire= datetime.now(timezone.utc) + expires_delta
    else:
        expire= datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp":expire,"type":"refresh"})
    encoded_jwt= jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



