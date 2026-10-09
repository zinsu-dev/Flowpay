import uuid
from sqlalchemy import String, Integer, Float, Column, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import foreign, relationship
from database.database import Base 
from enum import Enum
from datetime import datetime

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

class TransactionStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class TransactionTypes(str, Enum):
    DEPOSIT = "deposit"
    TRANSFER = "transfer"
    WITHDRAWAL = "withdrawal"    


class Wallet(Base):
    __tablename__="wallet"
    id = Column(String, default=lambda: str(uuid.uuid4()), primary_key=True, nullable=False)
    user = relationship("User", back_populates="wallet")
    account_number = Column(String(10), unique=True, nullable=False)
    wallet_userId = Column(String, ForeignKey("user.userId"), unique=True)
    wallet_currency = Column(String, default=lambda: str("NGN"), nullable=False)
    wallet_available_balance = Column(Numeric(18, 2), nullable=False, default=0)
    wallet_status = Column(String, default=lambda: str("active"), nullable=False)
    ledger = relationship(
        "LedgerAccount",
        back_populates="wallet")
    sent_transactions = relationship(
    "Transaction",
    foreign_keys="Transaction.sender_wallet_id",
    back_populates="sender_wallet",)

    received_transactions = relationship(
    "Transaction",
    foreign_keys="Transaction.receiver_wallet_id",
    back_populates="receiver_wallet",)
    


class LedgerAccount(Base):
    __tablename__="ledger"
    id = Column(String, default=lambda: str(uuid.uuid4()), primary_key=True, nullable=False)
    wallet = relationship(
        "Wallet",
        back_populates="ledger")
    transaction = relationship(
    "Transaction",
    back_populates="ledger_entries",)
    
    transaction_id = Column(
        String,
        ForeignKey("transaction.id"),
        nullable=False,
    )
    entries_amount = Column(Numeric(18, 2), nullable=False, default=0)
    account_owners_type = Column(String, default="wallet", nullable=False)
    entries_id = Column(String, ForeignKey("wallet.id"), nullable=False)
    entries_type = Column(String, default=lambda:str("credit"), nullable=False)


class Transaction(Base):
    __tablename__="transaction"
    id = Column(String, default=lambda: str(uuid.uuid4()), primary_key=True, nullable=False)
    transaction_amount = Column(Numeric(18, 2), nullable=False, default=0)
    transaction_status = Column(String, default=lambda:str("pending"), nullable=False)
    currency = Column(String, ForeignKey("wallet.wallet_currency"), nullable=False)
    transaction_type = Column(String, default=lambda:str("deposit"), nullable=False)
    transaction_reference = Column(String, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    provider_reference = Column(String, unique=True,default=lambda: str(uuid.uuid4()), nullable=True)
    sender_wallet_id = Column(
        String,
        ForeignKey("wallet.id"),
        nullable=True
    )

    receiver_wallet_id = Column(
        String,
        ForeignKey("wallet.id"),
        nullable=False
    )

    sender_wallet = relationship(
        "Wallet",
        foreign_keys=[sender_wallet_id],
        back_populates="sent_transactions",
    )

    receiver_wallet = relationship(
        "Wallet",
        foreign_keys=[receiver_wallet_id],
        back_populates="received_transactions",
    )
    created_at = Column(DateTime, default=lambda: datetime.utcnow(), nullable=False)
    ledger_entries = relationship(
        "LedgerAccount",
        back_populates="transaction")
    
    
