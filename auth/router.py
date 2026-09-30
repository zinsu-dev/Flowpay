from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from auth.models import User, UserSession
from auth.schema import Signup, Login, Logout, ForgetPassword, Resetpassword
from auth.utils import hash_password, verify_password
from auth.auth import create_access_token, decode_token

router = APIRouter(
    tags=["auth"],
    prefix="/auth"
)

@router.post("/signup")
def user_register(request: Signup, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()

    if not user:
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
def login(request: Login, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="user not found"
        )
    if not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )

    access_token = create_access_token(user.userId)

    db.add(UserSession)
    db.flush()
    user.token = access_token


    db.commit()

    return {
        "message": "Login successful",
        "token": access_token
    }


@router.post("/logout")
def logout(request: Logout, db: Session = Depends(get_db)):
    user_id=decode_token(request.token)
    user = db.query(User).filter(User.userId == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="user not found"
        )
    if not user.token:
        raise HTTPException(
            status_code=401,
            detail="user is not logged in"
        )
    user.token=None
    db.commit()    
    return {
        "message": "Logout successful"
    }


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
