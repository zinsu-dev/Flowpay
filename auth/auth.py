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

Oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

algorithm =os.getenv("ALGORITHM", "HS256") 
secret_key = os.getenv("SECRET_KEY")
EXPIRE_MIN=30



def create_access_token(user_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MIN)
    payload = {
        "sub": str(user_id),
        "exp": expire
    }

    return jwt.encode(
        payload,
        secret_key,
        algorithm=algorithm
    )


def decode_token(token: str) -> str:
    try:
        payload = jwt.decode(
            token,
            secret_key,
            algorithms=[algorithm]
        )
        user_id = payload.get("sub")
        if not isinstance(user_id, str) or not user_id:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )
        

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Expired token"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
    return user_id

def get_current_user(
    token: str = Depends(Oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    user_id = decode_token(token)
    user = db.query(User).filter(
        User.userId == user_id,

    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid or revoked token"
        )
    return user
    




