from pydantic import BaseModel, EmailStr,String,Float,Integer,Boolean

class Signup(BaseModel):
    full_name:str
    username:str
    email:EmailStr
    transaction_pin:str
    password:str
    confirm_password:str

class Login(BaseModel):
    email:EmailStr
    password:str

class ForgetPassword(BaseModel):
    token:str
    new_password:str
    confirm_passwod:str

    
            







