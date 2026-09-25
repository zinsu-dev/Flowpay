import jwt 
from datetime import datetime, timezone,timedelta
from dotenv import load_dotenv
from fastapi import HTTPException, Depends
from database.database import get_db
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from auth.models import User
import os

load_dotenv()

Oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

algorithm =os.getenv("ALGORITHM", "HS256") 
secret_key = os.getenv("SECRT_KEY")
EXPIRE_MIN=30



def create_access_token(userId: str):
    expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MIN)
    payload = {
        "sub": userId,
        "exp": expire
    }

    token =jwt.encode(
        payload,
        secret_key,
        algorithm=algorithm
    )
    return token


def decode_token(token: str):
    try:
        payload =jwt.decode(
            token,
            secret_key,
            aLgorithms=[algorithm]
        )
        userId:str=payload.get("sub")
        if not userId:
            raise HTTPException(
                status_code=402,
                detail="Invalid userId"
            )
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
        status_code= 401,
        detail= "Expired token"
    ) 
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
    return userId

def get_current_user(token: str=Depends(Oauth2_scheme), db: Session=Depends(get_db)) -> User:
    userId=decode_token(token)

    user = db.query(User).filter(User.userId == userId).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return user
    




