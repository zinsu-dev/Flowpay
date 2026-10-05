from fastapi import FastAPI
from auth.router import router as auth
from wallet.router import router as wallet 

app = FastAPI()

app.include_router(auth)
app.include_router(wallet)