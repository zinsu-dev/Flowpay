from pydantic import AliasChoices, BaseModel, EmailStr, Field


class Signup(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    phone_number: str
    transaction_pin: int
    password: str 
    confirm_password: str


class Login(BaseModel):
    email: EmailStr
    password: str

class Logout(BaseModel):
    RefreshToken: str

class ForgetPassword(BaseModel):
    email: EmailStr


class Resetpassword(BaseModel):
    token: str
    new_password: str
    confirm_password: str

