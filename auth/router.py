from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from auth.models import User, UserSession
from auth.schema import Signup, Login, Logout, ForgetPassword, Resetpassword
from auth.utils import hash_password, verify_password
from auth.auth import create_access_token, decode_token,get_current_user
from wallet.account_number import generate_account_number
from wallet.model import Wallet
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["auth"],
    prefix="/auth"
)

@router.post("/signup")
def user_register(request: Signup, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email, User.username == request.username).first()
    phone_number = db.query(User).filter(User.phone_number == request.phone_number).first()

    if user:
        raise HTTPException(
            status_code=409,
            detail="email or username already exist"
        )

    if phone_number:
        raise HTTPException(
            status_code=409,
            detail="phone number already exist"
        )

    if request.password != request.confirm_password:
        raise HTTPException(
            status_code=422,
            detail="both password do not match"
        )
    password = hash_password(request.password)
    transaction_pin = hash_password(str(request.transaction_pin))

    if not request.transaction_pin ==4:
        raise HTTPException(
            status_code=422,
            detail="transaction pin must be at least 4 characters long"
        )

    user = User(
        first_name = request.first_name,
        last_name = request.last_name,
        username = request.username,
        email = request.email,
        transaction_pin = transaction_pin,
        phone_number = request.phone_number,
        password = password

    )


    db.add(user)
    db.flush()
    


    account_number = generate_account_number()
    wallet = Wallet(
        account_number=account_number,

    )
    db.add(wallet)
    db.commit()
   

    
    


    return {
        "message": "Account created successful",
        "id": user.userId,
        "account_number": account_number
    
    }


@router.post("/login")
def login(request: Login, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )

    access_token = create_access_token(user.userId)
    refresh_token = create_access_token(str(user.userId))

    session = UserSession(
        userId=str(user.userId),
        token=refresh_token,
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    return {
        "message": "Login successful",
        "token": access_token,
        "refresh_token": refresh_token,
    }


@router.post("/logout")
def logout(request: Logout, db: Session = Depends(get_db)):
    session = db.query(UserSession).filter(UserSession.token == request.RefreshToken).first()

    if session:
        db.delete(session)
        db.commit()
    return {"message": "Logged out successfully"}


@router.post("/forgetpassword")
def forget_password(request: ForgetPassword, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="user not found"
        )
    reset_token = create_access_token(str(user.userId))
    return {
        "token": reset_token
    }


@router.post("/resetpassword")
def resetpassword(request: Resetpassword, db: Session = Depends(get_db)):
    user_id = decode_token(request.token)
    user = db.query(User).filter(User.userId == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    if request.new_password != request.confirm_password:
        raise HTTPException(
            status_code=422,
            detail="password do not match"
        )

    user.password = hash_password(request.new_password)
    user.token = None
    db.commit()
    return {
        "message": "password reset successful"
    }


@router.post("/token")
def get_user_0Auth2PasswordBearer(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.username).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="user not found"
        )
    if not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect password"
        )
    create_token = create_access_token(str(user.userId))
    return{
        "access_token": create_token,
        "token_type": "bearer"
    }

@router.get("/me")
def get_current_user(get_current_user: User=Depends(get_current_user), db:Session=Depends(get_db)):
    return{
        "userid": get_current_user.userId,
        "first_name": get_current_user.first_name,
        "last_name": get_current_user.last_name,
        "username": get_current_user.username,
        "email": get_current_user.email,
        "phone_number": get_current_user.phone_number,
        "transaction_pin": get_current_user.transaction_pin,
        "Password": get_current_user.password,
    }

    