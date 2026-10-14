from decimal import Decimal
from fastapi import HTTPException
from sqlalchemy.orm import Session
from wallet.model import Transaction, Wallet, WalletStatus, LedgerAccount
from wallet.schema import DepositRequest

def process_deposit(request: DepositRequest, wallet: Wallet, db: Session):
    try:
        amount = Decimal(str(request.transaction_amount))

        if amount <= 0:
            raise HTTPException(
                status_code=400,
                detail="Amount must be greater than zero"
            )

        if wallet.wallet_currency != request.currency:
            raise HTTPException(
                status_code=400,
                detail="currency mismatched"
            )


        transaction = Transaction(
            transaction_amount = request.transaction_amount,
            currency = request.currency,
            transaction_type = "deposit",
            sender_wallet_id = None,
            receiver_wallet_id = wallet.id,
            transaction_status = "pending"
            
        )

    

        db.add(transaction)
        db.commit()
        db.refresh(transaction)



        return {
                "message": "Deposit initiated",
                "status": "pending",
                "transaction_reference": transaction.transaction_reference,
                "amount": str(transaction.transaction_amount),
                "currency": transaction.currency,
            }
    
    except Exception:
        db.rollback()
        raise



def complete_deposit(transfer_reference: str, provider_reference: str, db: Session):
    transaction = db.query(Transaction).filter(Transaction.transaction_reference == transfer_reference).with_for_update().first()

    try:
        if not transaction:
            raise HTTPException(
            status_code=404,
            detail="no transaction found."
        )

        if transaction.transaction_status == "completed":
            return {
                "message": "transaction is completed already",
                "status": "completed"
            }

        if transaction.transaction_type != "deposit":
            raise HTTPException(
                status_code=400,
                detail="Invalid transaction type"

            )

        if transaction.transaction_status != "pending":
            raise HTTPException(
                status_code=400,
                detail="transaction cannot be compleeted"
            )

        receiver = db.query(Wallet).filter(Wallet.id == transaction.receiver_wallet_id).with_for_update().first()

        if not receiver:
            raise HTTPException(
                status_code=404,
                detail="no wallet found"
            )

        receiver.wallet_available_balance += (transaction.transaction_amount)

        ledger_entry = LedgerAccount(
                transaction_id = transaction.id,
                entries_amount = transaction.transaction_amount,
                account_owners_type = "wallet",
                entries_id = receiver.id,
                entries_type = "credit"
            )

        transaction.transaction_status = "completed"
        transaction.provider_reference = provider_reference

        db.add(ledger_entry)
        db.commit()
        db.refresh(receiver)

        return { "message": "Deposit completed successfully",
                "status": "completed",
                "transaction_reference": transaction.transaction_reference,
                "amount": str(transaction.transaction_amount), 
                "currency": transaction.currency, }

    except Exception:
        db.rollback()
        raise 



def fail_deposit(transaction_reference: str, db: Session):
    try:
        transaction = db.query(Transaction).filter(Transaction.transaction_reference == transaction_reference).with_for_update().first()

        if not transaction:
            raise HTTPException(
                status_code=404,
                detail="no transaction found"
            )
        if transaction.transaction_status == "completed":
            raise HTTPException(
                status_code=409,
                detail="deposit is completed already"
            )

        if transaction.transaction_status == "failed":
            return {
                "message": "Deposit already mark as failed",
                "status": "Failed"
            }
        if transaction.transaction_status != "pending":
            raise HTTPException(
                status_code=400,
                detail="transaction cannot be failed"

            )

        transaction.transaction_status = "failed"

        db.commit()

        return {
            "message": "Deposit failed",
            "status": "failed"
        }

    except Exception:
        db.rollback()
        raise
    

