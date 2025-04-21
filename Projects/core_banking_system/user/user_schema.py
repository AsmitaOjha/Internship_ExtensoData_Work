from sqlalchemy import Column, BigInteger, String, Date,Boolean
from sqlalchemy.orm import relationship
from database import MySQLConnection
from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class User(MySQLConnection.Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(10), nullable=False)
    phone_number = Column(String(20), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    state = Column(String(255), nullable=False)
    country = Column(String(255), nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)

    # ✅ Match this with `back_populates="user"` in Account
    accounts = relationship("Account", back_populates='user')

class UserCreate(BaseModel):
    name: str
    date_of_birth: date
    gender: str
    phone_number: str
    email: EmailStr
    password: str
    city: str
    state: str
    country: str
    # is_admin: bool 
    is_admin: Optional[bool] = False

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    date_of_birth: date
    gender: str
    phone_number: str
    city: str
    state: str
    country: str
    is_admin: bool
    class Config:
        from_attributes = True
