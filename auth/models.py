from sqlalchemy import String, Integer, Float, Boolean, Column, DateTime
from sqlalchemy.orm import relationship
from database.database import Base
import uuid
from enum import Enum
from datetime import datetime, timezone

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

class User(Base):
    __tablename__="user"
    first_name = Column(String, nullable=False)
    last_name =  Column(String, nullable=False)
    userId = Column(String, default=lambda: str(uuid.uuid4()), primary_key=True, nullable=False)
    role = Column(String, default=lambda:str("user"))
    username = Column(String, unique=True, nullable=False)
    wallet = relationship("Wallet", back_populates="user")
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String,nullable=True, unique=True)
    transaction_pin = Column(Integer, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    