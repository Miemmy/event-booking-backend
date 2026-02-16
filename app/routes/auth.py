from fastapi import APIRouter, HTTPException, status , Depends
from app.models.user import User
from fastapi.security import OAuth2PasswordRequestForm # this is to make swagger ui understand our authentication flow and show the login form in the docs, but we will not use it in our code, we will use our own UserLogin schema instead
from app.schemas.user_schema import UserCreate, UserOut, UserLogin
from app.utils.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    hash_password
)

router= APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate): #basically this is what our user input should look like
    existing_user= await User.find_one(User.email==user.email)
    if existing_user:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
            
        )
    
   
    hashed_pwd= hash_password(user.password)

    new_user= User(
        username=user.username,
        email=user.email,
        password_hash=hashed_pwd,
        role=user.role
    )

    #saving to db....
    await new_user.insert()
    return new_user #should look like UserOut tbh

@router.post("/login")
async def login(user_details: OAuth2PasswordRequestForm = Depends()):
    user= await User.find_one(User.email==user_details.username) # well now it's username and not email because: user= await User.find_one(User.email==user_details.email)

    if not user or not verify_password(user_details.password, user.password_hash):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials, lease check your email and password"
        )
    access_token=create_access_token(data={"sub": str(user.id), "role":user.role})
    
    refresh_token= create_refresh_token(
        data={"sub": str(user.id), "role":user.role}
    )

    return{
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


