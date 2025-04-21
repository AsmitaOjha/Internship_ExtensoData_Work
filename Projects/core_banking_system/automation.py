import random
from datetime import datetime
import requests
from faker import Faker
import time

fake = Faker()

BASE_URL = "http://localhost:8000"  # Change as needed

NUM_USERS = 30
ACCOUNT_TYPES = ["Saving", "Current", "Fixed Deposit"]
TRANSACTION_TYPES = ["deposit", "withdraw", "transfer"]
REMARKS = [
    "travel & ticketing", "food", "clz/school fee", "recharge",
    "rent", "cloth and accessories", "clothes", "other"
]

account_ids = []  # Will store account numbers

# ------------------------- #
# User + Account Creation   #
# ------------------------- #

def register_user():
    dob = fake.date_of_birth(minimum_age=18, maximum_age=70)
    user_data = {
        "name": fake.name(),
        "date_of_birth": dob.isoformat(),
        "gender": random.choice(["Male", "Female", "Other"]),
        "phone_number": fake.phone_number(),
        "email": fake.unique.email(),
        "password": "Password123!",
        "city": fake.city(),
        "state": fake.state(),
        "country": fake.country(),
        "is_admin": False
    }
    res = requests.post(f"{BASE_URL}/user/register", json=user_data)
    if res.status_code == 200 or res.status_code == 201:
        user_id = res.json().get("id")
        print(f"✅ Registered: {user_data['email']}")
        return user_id
    else:
        print(f"❌ Failed to register {user_data['email']}: {res.text}")
        return None

def create_account(user_id: int):
    account_data = {
        "account_type": random.choice(ACCOUNT_TYPES),
        "account_status": "Active",
        "account_balance": round(random.uniform(500, 100000), 2),
        "user_id": user_id
    }
    res = requests.post(f"{BASE_URL}/account/create", json=account_data)
    if res.status_code == 200 or res.status_code == 201:
        account_number = res.json().get("account_number")  # Must return this!
        print(f"🏦 Account created: {account_number}")
        account_ids.append(account_number)
    else:
        print(f"❌ Failed to create account: {res.text}")

# ------------------------- #
# Transaction Creation      #
# ------------------------- #

def create_transaction():
    sender_id = random.choice(account_ids)
    transaction_type = random.choice(TRANSACTION_TYPES)
    amount = round(random.uniform(500, 1000), 2)
    remark = random.choice(REMARKS)

    receiver_id = None
    if transaction_type == "transfer":
        receiver_id = random.choice([acc for acc in account_ids if acc != sender_id])
    
    payload = {
        "transaction_type": transaction_type,
        "amount": amount,
        "remark": remark,
        "sender_account_id": sender_id,
        "receiver_account_id": receiver_id
    }

    res = requests.post(f"{BASE_URL}/transactions/create", json=payload)
    if res.status_code == 200 or res.status_code == 201:
        print(f"💸 {transaction_type.title()} of ${amount} from {sender_id} {'to ' + receiver_id if receiver_id else ''}")
    else:
        print(f"❌ Transaction failed: {res.text}")

# ------------------------- #
# Main Runner               #
# ------------------------- #

#make transactions
def storeAccounts():
    res = requests.get(f"{BASE_URL}/account/all")
    if res.status_code == 200:
        accounts = res.json()
        for account in accounts:
            account_ids.append(account["account_number"])
    else:
        print(f"❌ Failed to fetch accounts: {res.text}")



if __name__ == "__main__":
    # Register users and create accounts
    for _ in range(NUM_USERS):
        user_id = register_user()
        if user_id:
            create_account(user_id)
        time.sleep(0.5)  # Add a short delay between user registrations

    storeAccounts()
    time.sleep(1)  

    # Create transactions
    for _ in range(NUM_USERS * 3): 
        if len(account_ids) >= 2:
            create_transaction()
        time.sleep(0.3)  