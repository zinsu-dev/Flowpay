from database.database import get_db
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from wallet.model import Transaction, Wallet, WalletStatus
from wallet.schema import DepositRequest

def process_deposit(request: DepositRequest, db: Session):
    receiver = db.query(Wallet).filter(Wallet.id == request.receiver_wallet_id).first()

    # if not receiver:
    #     raise HTTPException(
    #         status_code=404,
    #         detail="receiver not found"
    #     )

    transaction = Transaction(
        transaction_amount = request.transaction_amount,
        currency = request.currency,
        transaction_type = "deposit",
        sender_wallet_id = None,
        receiver_wallet_id = request.receiver_wallet_id,
        transaction_status = "completed"
        
    )

    
    receiver.wallet_available_balance += request.transaction_amount
    

    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return {
        "message": "transaction successful",
        "status": "completed",
        "balance": receiver.wallet_available_balance,
        "Name": receiver.user.first_name + " " + receiver.user.last_name

    }



# def process_transfer()
