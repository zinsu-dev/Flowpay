from pydantic import BaseModel, Field
from decimal import Decimal 


class WalletResponse(BaseModel):
    wallet_id : str
    wallet_userId : str


class DepositRequest(BaseModel):
    transaction_amount: Decimal = Field(gt=0,description="Amount to deposit")
    currency: str = "NGN"
    transaction_type: str = "deposit"
    sender_wallet_id: None
    receiver_wallet_id: str
