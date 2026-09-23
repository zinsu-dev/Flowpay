from fastapi import APIRouter
from schema import Signup, Login, ForgetPassword, Resetpassword
from sqlalchemy.orm import Session
from fastapi import Depends
from database.database import get_db
import main


router = APIRouter(
    prefix= "/auth",
    tags=["auth"]

)

@router.post("/user")
def user_registeration(request: Signup, db: Session=Depends(get_db)):
    return main.user_register(request, db)



