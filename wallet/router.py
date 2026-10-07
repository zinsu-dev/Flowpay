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

@router.get("/wallet")
def get_user_wallet(currentuser: str=Depends(get_current_user), db: Session=Depends(get_db)):
    get_wallet = db.query(Wallet).filter(Wallet.wallet_userId == currentuser.userId).first()

    if not get_wallet:
        raise HTTPException(
            status_code=404,
            detail="not found!"
        )
    return get_wallet(
        "wallet_id",
        "wallet_available_balance",
        "wallet_currency",
        "account_balance",
        "wallet_status"
    )



