from dataclasses import field

from pydantic import BaseModel
from decimal import Decimal 


class WalletResponse(BaseModel):
    wallet_id : str
    wallet_userId : str


class DepositRequest(BaseModel):
    transaction_amount: Decimal = field(gt=0, description="Amount to deposit")
    currency: str = "NGN"
    transaction_type: str = "deposit"
    sender_wallet_id: str
    receiver_wallet_id: str
