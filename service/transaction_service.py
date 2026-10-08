from database.database import get_db
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from wallet.model import Transaction, Wallet
from wallet.schema import DepositRequest

def process_deposit(request: DepositRequest, db: Session):
    receiver = db.query(Wallet).filter(Wallet.wallet_id == request.receiver_wallet_id).first()

    if not receiver:
        raise HTTPException(
            status_code=404,
            detail="sender or receiver not found"
        )
    if receiver.wallet_status != "active":
        raise HTTPException(
            status_code=400,
            detail="Wallet not active"
        )

    if receiver.wallet_currency != request.currency:
        raise HTTPException(
            status_code=400,
            detail="currency mismatch"
        )

    transaction = Transaction(
        transaction_amount = request.transaction_amount,
        currency = request.currency,
        transaction_type = "`deposit",
        sender_wallet_id = None,
        receiver_wallet_id = request.receiver_wallet_id
        transaction_status = "pending"
        

    )

    
    receiver.wallet_available_balance += request.transaction_amount
    

    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


def process_transfer(r)
