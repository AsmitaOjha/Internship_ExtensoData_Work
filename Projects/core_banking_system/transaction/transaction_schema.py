from sqlalchemy import Column, BigInteger, DateTime, Enum, ForeignKey, DECIMAL, String, func
from sqlalchemy.orm import relationship
from database import MySQLConnection
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Literal
from sqlalchemy import Index

class Transaction(MySQLConnection.Base):
    __tablename__ = "transactions"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    transaction_type = Column(Enum("deposit", "withdraw", "transfer"), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    transaction_time = Column(DateTime, nullable=False, default=func.now())
   # remark = Column(String(255), nullable=False)  # match SQL NOT NULL
    remark = Column(Enum(
    "travel & ticketing",
    "food",
    "clz/school fee",
    "recharge",
    "rent",
    "cloth and accessories",
    "clothes",
    "other",
    name="remark_enum"
    ), nullable=False)
    status = Column(Enum("Completed", "Failed", "Pending"), nullable=True)

    # Foreign Keys to accounts table
    sender_account_id = Column(String, ForeignKey('accounts.account_number', ondelete='CASCADE'), nullable=False)
    receiver_account_id = Column(String, ForeignKey('accounts.account_number', ondelete='CASCADE'), nullable=True)

    # Relationships
    sender_account = relationship("Account", foreign_keys=[sender_account_id])
    receiver_account = relationship("Account", foreign_keys=[receiver_account_id])

    __table_args__ = (
    Index('idx_sender_account', 'sender_account_id'),
    Index('idx_receiver_account', 'receiver_account_id'),
    Index('idx_transaction_type', 'transaction_type'),
)

# Pydantic Input Model
class TransactionCreate(BaseModel):
    transaction_type: Literal["deposit", "withdraw", "transfer"]
    amount: float
    remark: Literal[
    "travel & ticketing",
    "food",
    "clz/school fee",
    "recharge",
    "rent",
    "cloth and accessories",
    "clothes",
    "other",
    ]
   # status: Optional[Literal["Completed", "Failed", "Pending"]] = "Completed"
    sender_account_id: str
    receiver_account_id: Optional[str] = None

    

# Pydantic Output Model
class TransactionOut(BaseModel):
    id: int
    transaction_type: str
    amount: float
    transaction_time: datetime
    remark: str
    status: str
    sender_account_id: str
    receiver_account_id: Optional[str]

    class Config:
        from_attributes = True
