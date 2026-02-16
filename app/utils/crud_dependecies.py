from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt  
from jwt import PyJWTError # This handles the specific error from PyJWT
from app.utils.security import SECRET_KEY, ALGORITHM
from app.models.user import User

oauth2_scheme= OAuth2PasswordBearer(tokenUrl="/auth/login") 

async def get_current_user(token:str= Depends(oauth2_scheme)) -> User:
    credentials_exception= HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"}
    )

    

    try:
        payload= jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str= payload.get("sub")
        if user_id is None:
            raise credentials_exception
        
    except PyJWTError:
        raise credentials_exception
    
    user = await User.get(user_id)
    if user is None:
        raise credentials_exception
    
    return user

async def require_organizer(current_user: User= Depends(get_current_user)) ->User:
    if current_user.role!="organizer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action"
        )
    return current_user
