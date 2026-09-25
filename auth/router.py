from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from auth.model import User
from auth.schema import Signup, Login, ForgetPassword, Resetpassword
from auth.utils import hash_password, verify_password
from auth.auth import create_access_token

router = APIRouter(
    tags=["auth"],
    prefix="/auth"
)



@router.post("/signup")
def user_register(request: Signup, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()

    if user:
        raise HTTPException(
            status_code=409,
            detail="email already exist"
        )
    if request.password != request.confirm_password:
        raise HTTPException(
            status_code=422,
            detail="both password do not match"
        )
    password = hash_password(request.password)

    user = User(
        first_name = request.first_name,
        last_name = request.last_name,
        username = request.username,
        email = request.email,
        transaction_pin = request.transaction_pin,
        password = password

    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "Account created successful",
        "id": user.userId
    }

@router.post("/login")
def login_user(request: Login, db: Session=Depends(get_db)):
    user = db.query(User).filter(User.email==request.email).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect credentials"
        )

    create_token = create_access_token(
        user.userId
    )

    return {
        "message": "Login successful",
        "token": create_token
    }
