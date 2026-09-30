import uuid
from sqlalchemy import String, Integer, Float, Column, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base 
from enum import Enum

class WalletCurrency(str, Enum):
    NIGERIA_NGN = "NGN"
    US_DOLLAR = "USD"
    EURO = "EUR"
    YUAN = "RMB"

class WalletStatus(str, Enum):
    ACTIVE = "active"
    FROZEN = "frozen"
    CLOSED = "closed"

class LedgerEntryTypes(str, Enum):
    CREDIT = "credit"
    DEBIT = "debit"

class Wallet(Base):
    __tablename__="wallet"
    id = Column(String, default=lambda: str(uuid.uuid4()), primary_key=True, nullable=False)
    user = relationship("User", back_populates="wallet")
    wallet_userId = Column(String, ForeignKey("user.userId"), unique=True)
    wallet_currency = Column(String, default=lambda: str("NGN"), nullable=False)
    wallet_available_balance = Column(Float, nullable=False, default=0)
    wallet_status = Column(String, default=lambda: str("active"), nullable=False)
    ledger = relationship("LedgerAccount", back_populates="wallet")


class LedgerAccount(Base):
    __tablename__="ledger"
    id = Column(String, default=lambda: str(uuid.uuid4()), primary_key=True, nullable=False)
    wallet = relationship("Wallet", back_populates="ledger")
    entries_amount = Column(Float, nullable=False, default=0)
    account_owners_type = Column(String, default="wallet", nullable=False)
    entries_id = Column(String, default=lambda: str(uuid.uuid4()))
    entries_type = Column(String, default=lambda:str("credit"), nullable=False)



    
