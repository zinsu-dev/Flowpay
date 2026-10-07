from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from database.database import get_db
from wallet.model import Wallet, LedgerAccount
from wallet.account_number import generate_account_number
from auth.auth import get_current_user


router=APIRouter(
    tags=["/wallet"],
    prefix="/wallet"
)

@router.get("/user_wallet_details")
def get_user_wallet(currentuser: str=Depends(get_current_user), db: Session=Depends(get_db)):
    get_wallet = db.query(Wallet).filter(Wallet.wallet_userId == currentuser.userId).first()

    if not get_wallet:
        raise HTTPException(
            status_code=404,
            detail="not found!"
            )

    return {
        "wallet_id": get_wallet.id,
        "wallet_available_balance": get_wallet.wallet_available_balance,
        "wallet_currency": get_wallet.wallet_currency,
        "account_number": get_wallet.account_number,
        "wallet_status": get_wallet.wallet_status
    }

@router.get("/user_account_number")
def get_user_account_number(currentuser: str=Depends(get_current_user), db: Session=Depends(get_db)):
    user = db.query(Wallet).filter(Wallet.wallet_userId == currentuser.userId).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="user account not found"
        )
    return {
        "Account_number": user.account_number

    }
        



