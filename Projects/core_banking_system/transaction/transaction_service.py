from sqlalchemy.orm import Session
from fastapi import HTTPException
from transaction.transaction_schema import TransactionCreate, Transaction
from account.account_schema import Account
from decimal import Decimal
from sqlalchemy import func, or_
from sqlalchemy import extract

def get_user_transaction_summary(db: Session, user_id: int):
    #get the account number linked to this user
    user_account = db.query(Account).filter(Account.user_id == user_id).first()

    if not user_account:
        return {"error": "User account not found."}
    
    account_no = user_account.account_number

    total_sent = db.query(func.sum(Transaction.amount)).filter(
        Transaction.sender_account_id == account_no).scalar() or 0
    
    total_received = db.query(func.sum(Transaction.amount)).filter(
        Transaction.receiver_account_id == account_no).scalar() or 0
    
    total_transactions = db.query(Transaction).filter(
        or_(
            Transaction.sender_account_id == account_no,
            Transaction.receiver_account_id == account_no
        )
    ).count()

    last_transaction_date = db.query(func.max(Transaction.transaction_time)).filter(
        or_(
            Transaction.sender_account_id == account_no,
            Transaction.receiver_account_id == account_no
        )
    ).scalar()

    return{
        "total_transactions": total_transactions,
        "total_sent": float(total_sent),
        "total_received": float(total_received),
        "last_transaction_date": last_transaction_date
    }

def get_monthly_transaction_trends(db: Session, account_number: str):
    sent_query = db.query(
        func.concat(func.year(Transaction.transaction_time), '_', func.lpad(func.month(Transaction.create_at), 2, '0')).label('month'),
        func.sum(Transaction.amount).label('sent')
        ).filter(Transaction.sender_account_id == account_number).group_by('month')
    
    received_query = db.query(
        func.concat(func.year(Transaction.transaction_time),'_', func.lpad(func.month(Transaction.transaction_time),2, "0")).label('month'),
        func.sum(Transaction.amount).label('received')
        ).filter(Transaction.receiver_account_id == account_number).group_by('month')

    #collect into dicts for easy merging
    sent_data = {row.month: float(row.sent) for row in sent_query}
    received_data = {row.month: float(row.received) for row in received_query}

    #merge both into a unified structure
    all_months = sorted(set(sent_data.keys()) | set(received_data.keys()))
    trends = []

    for month in all_months:
        trends.append({
            "month": month,
            "sent": sent_data.get(month, 0),
            "received": received_data.get(month, 0)
        })
    
    return trends

def create_transaction(db: Session, transaction_data: TransactionCreate):
    # Initialize default status
    transaction_status = "Pending"

    try:
        sender = db.query(Account).filter(
            Account.account_number == transaction_data.sender_account_id
        ).first()

        if not sender:
            raise HTTPException(status_code=404, detail="Sender account not found.")

        amount = Decimal(transaction_data.amount)

        if transaction_data.transaction_type == "deposit":
            sender.account_balance += amount
            transaction_status = "Completed"

        elif transaction_data.transaction_type == "withdraw":
            if sender.account_balance < amount:
                transaction_status = "Failed"
                raise HTTPException(status_code=400, detail="Insufficient balance.")
            sender.account_balance -= amount
            transaction_status = "Completed"

        elif transaction_data.transaction_type in ["transfer", "payment"]:
            if sender.account_balance < amount:
                transaction_status = "Failed"
                raise HTTPException(status_code=400, detail="Insufficient balance.")
            sender.account_balance -= amount

            receiver = db.query(Account).filter(
                Account.account_number == transaction_data.receiver_account_id
            ).first()

            if not receiver:
                transaction_status = "Failed"
                raise HTTPException(status_code=404, detail="Receiver account not found.")

            receiver.account_balance += amount
            db.add(receiver)
            transaction_status = "Completed"

        # Create transaction record
        transaction = Transaction(
            transaction_type=transaction_data.transaction_type,
            amount=amount,
            remark=transaction_data.remark,
            status=transaction_status,  # Auto-set here
            sender_account_id=transaction_data.sender_account_id,
            receiver_account_id=transaction_data.receiver_account_id
        )

        db.add(sender)
        db.add(transaction)
        db.commit()
        db.refresh(transaction)

        return transaction

    except HTTPException as e:
        # In case of failure, record transaction with "Failed" status
        transaction = Transaction(
            transaction_type=transaction_data.transaction_type,
            amount=Decimal(transaction_data.amount),
            remark=transaction_data.remark,
            status="Failed",
            sender_account_id=transaction_data.sender_account_id,
            receiver_account_id=transaction_data.receiver_account_id
        )
        db.add(transaction)
        db.commit()
        db.refresh(transaction)

        raise e  # Re-raise the original exception to maintain FastAPI's behavior

def get_all_transactions(db: Session):
    transactions = db.query(Transaction).all()
    return transactions

def get_transaction_by_id(db: Session, user_id: int):
    user_account = db.query(Account).filter(Account.user_id == user_id).first()

    if not user_account:
        return {"error": "User account not found."}

    account_no = user_account.account_number

    transactions = db.query(Transaction).filter(
        or_(
            Transaction.sender_account_id == account_no,
            Transaction.receiver_account_id == account_no
        )
    ).order_by(Transaction.transaction_time.desc()).all()

    if not transactions:
        raise HTTPException(status_code=404, detail="Transactions not found.")
    
    return transactions