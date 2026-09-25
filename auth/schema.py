from pydantic import BaseModel, EmailStr

class Signup(BaseModel):
    first_name:str
    last_name:str
    username:str
    email:EmailStr
    phone_number:str
    transaction_pin:str
    password:str
    confirm_password:str


class Login(BaseModel):
    email:EmailStr
    password:str

class ForgetPassword(BaseModel):
    email:EmailStr

class Resetpassword(BaseModel):
     token:str
     new_password:str
     confirm_passwod:str
    


            







