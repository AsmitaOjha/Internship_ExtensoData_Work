from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from account.account_schema import AccountCreate, AccountOut
from account.account_service import create_account, view_account,get_all_accounts, get_account_by_user_id


account_router = APIRouter()

@account_router.post("/create", response_model=AccountOut)
def account_creation(account_data: AccountCreate, db: Session = Depends(get_db)):
    try:
        new_account = create_account(db, account_data)
        return new_account
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@account_router.get("/view/{account_number}", response_model=AccountOut)
def get_account(account_number: str, db: Session = Depends(get_db)):
    try:
        account = view_account(db, account_number)
        return account
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@account_router.get("/all",)
def get_account( db: Session = Depends(get_db)):
    try:
        accounts = get_all_accounts(db);
        return accounts
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@account_router.get("/check/{user_id}", response_model=AccountOut)
def account_check_for_user_id(user_id: int, db: Session = Depends(get_db)):
    try:
        account = get_account_by_user_id(db, user_id)  # pass db!
        return account
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
