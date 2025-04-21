from sqlalchemy import Column, BigInteger, DateTime, Enum, String, ForeignKey, DECIMAL, func, Integer
from sqlalchemy.orm import relationship
from database import MySQLConnection
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Literal

# SQLAlchemy model
class Account(MySQLConnection.Base):
    __tablename__ = "accounts"

    serial_number = Column(Integer, unique=True, autoincrement=True)
    account_number = Column(String(20), primary_key=True)
    account_type = Column(Enum("Saving", "Current", "Fixed Deposit"), nullable=False, default="Saving")
    account_status = Column(Enum("Active", "Closed"), nullable=False)
    account_balance = Column(DECIMAL(10, 2), nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=func.now())
    closed_at = Column(DateTime, nullable=True)

    # Foreign keys
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
   # transaction_id = Column(BigInteger, nullable=True)  # nullable for now

    # Relationships
    user = relationship("User", back_populates='accounts')
    # transactions = relationship("Transaction", back_populates='accounts')

    sent_transactions = relationship("Transaction", foreign_keys="[Transaction.sender_account_id]", back_populates="sender_account")
    received_transactions = relationship("Transaction", foreign_keys="[Transaction.receiver_account_id]", back_populates="receiver_account")



# Pydantic input model (only needed fields)
class AccountCreate(BaseModel):
    account_type: Literal["Saving", "Current", "Fixed Deposit"]
    account_status: Literal["Active", "Closed"]
    account_balance: float
    user_id: int
    #transaction_id: Optional[int] = None


# Nested Pydantic model for user in output
class UserSummary(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True
        # orm_mode = True


# Output model with nested user
class AccountOut(BaseModel):
    account_number: str
    account_type: str
    account_status: str
    account_balance: float
    created_at: datetime
    closed_at: Optional[datetime]
    user: UserSummary                # nested user
   # transaction_id: Optional[int]

    class Config:
        from_attributes = True
        # orm_mode = True
