from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from transaction.transaction_schema import TransactionCreate, TransactionOut
from transaction.transaction_service import create_transaction,get_all_transactions,get_transaction_by_id
from database import get_db

#transaction_router = APIRouter(prefix="/transaction", tags=["Transactions"])
transaction_router = APIRouter()

@transaction_router.post("/create", response_model=TransactionOut)
def create_transaction_endpoint(transaction_data: TransactionCreate, db: Session = Depends(get_db)):
    return create_transaction(db, transaction_data)


@transaction_router.get("/all")
def get_all_transaction(db: Session = Depends(get_db)):
    transactions = get_all_transactions(db)
    return transactions


@transaction_router.get("/user/{user_id}")
def get_user_transaction(user_id: int, db: Session = Depends(get_db)):
    print(f"Fetching transactions for user_id: {user_id}")
    transactions = get_transaction_by_id(db, user_id)
    return transactions