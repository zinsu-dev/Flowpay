from sqlalchemy import String, Integer, Float, Boolean, Column, DateTime
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
    userId = Column(default=lambda: str(uuid.uuid4), primary_key=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    transaction_pin = Column(Integer, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    