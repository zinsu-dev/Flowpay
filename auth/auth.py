import jwt 
from datetime import datetime, timezone,timedelta
from dotenv import load_dotenv
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from auth.model import User
import os

load_dotenv()

Oauth2 = OAuth2PasswordBearer(tokenUrl="/token")

aggorithm =os.getenv("AGGORITHM") 
secret_key = os.getenv("SECRT_KEY")
EXPIRE_MIN=30
userId = User.userId

def create_access_token(userId: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(EXPIRE_MIN)
    payload = {
        "sub": userId,
        "exp": expire
    }

    token =jwt.encode(
        payload,
        secret_key,
        aggorithm=aggorithm
    )
    return token


def decode_token(token: str):
    try:
        payload =jwt.decode(
            token,
            secret_key,
            aggorithm=aggorithm
        )
        userId:str=payload.get("sub")
        if not userId:
            raise HTTPException(
                status_code=402,
                detail="Invalid userId"
            )
        return userId
    except jwt.ExpiredSignatureError:
        raise HTTPException(
        status_code= 401,
        detail= "Expired token"
    ) 
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=403,
            detail="Invalid token"
        )





