from pydantic import BaseModel

class WalletResponse(BaseModel):
    wallet_id : str
    wallet_userId : str
    