import streamlit as st
import requests
from datetime import date
import pandas as pd
import time
import plotly.express as px
from collections import defaultdict

# Base URL for backend API
BASE_URL = "http://localhost:8000"

# ------------------- User Check ------------------- #
def check_user_exists(email):
    response = requests.get(f"{BASE_URL}/user/exists", params={"email": email})
    return response.status_code == 200 and response.json().get("exists", False)

# ------------------- Register Form ------------------- #
def register_form():
    st.header("User Registration Form")

    with st.form("registration_form"):
        name = st.text_input("Full Name")
        date_of_birth = st.date_input("Date of Birth", min_value=date(1900, 1, 1), max_value=date.today(), value=date(2000, 1, 1))
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        phone_number = st.text_input("Phone Number")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        city = st.text_input("City")
        state = st.text_input("State")
        country = st.text_input("Country")

        submit = st.form_submit_button("Submit Registration")

    if submit:
        if password != confirm_password:
            st.error("Passwords do not match. Please try again.")
            return

        if check_user_exists(email):
            st.error("User already exists. Please login.")
            if st.button("Go to Login"):
                st.session_state.page = "login"
            return

        payload = {
            "name": name,
            "date_of_birth": str(date_of_birth),
            "gender": gender,
            "phone_number": phone_number,
            "email": email,
            "password": password,
            "city": city,
            "state": state,
            "country": country
        }

        try:
            res = requests.post(f"{BASE_URL}/user/register", json=payload)
            if res.status_code in [200, 201]:
                st.success("Registration Successful! Redirecting to login...")
                time.sleep(2)
                st.session_state.page = "login"
                st.rerun()
            else:
                st.error(res.json().get("detail", "Registration failed."))
        except Exception as e:
            st.error(f"An error occurred: {e}")
   

# ------------------- Login Form ------------------- #
def login_form():
    st.header("User Login")

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Submit Login")

    if submit:
        payload = {"email": email, "password": password}

        try:
            res = requests.post(f"{BASE_URL}/auth/login", json=payload)
            if res.status_code == 200:
                user_data = res.json()

                user_name = user_data.get("name", "User")
                user_id = user_data.get("user_id")
                is_admin = user_data.get("is_admin", False)


                st.success(f"Welcome, {user_name}!")
                st.info(f"Your **User ID is `{user_id}`**. Please keep this saved for future use (e.g., account creation, transactions).")
                time.sleep(2)

                # Save user data in session
                st.session_state.user = user_data

                
                # Redirect based on role
                if is_admin:
                    st.session_state.page = "admin_dashboard"
                else:
                    res = requests.get(f"{BASE_URL}/account/check/{user_id}")
                    if res.status_code == 200:
                        account = res.json()
                        st.session_state.account_number = account["account_number"]
                        st.session_state.account_created = True
                        st.session_state.page= "account_dashboard"
                     
                    else:
                        st.session_state.page = "user_dashboard"
                    

                st.rerun()
            else:
                st.error(res.json().get("detail", "Invalid credentials."))
        except Exception as e:
            st.error(f"An error occurred during login: {e}")
    navigation_footer()


# ------------------- Admin Dashboard ------------------- #
def admin_dashboard():
    st.title("🔐 Admin Dashboard - Laxmi Bank")
    st.write("Welcome to the Admin Dashboard. Here you can manage users and accounts.")

    # Section 1: View All Users
    st.subheader("👤 All Registered Users")
    user_data = pd.DataFrame()
    try:
        res = requests.get(f"{BASE_URL}/user/all")
        if res.status_code == 200:
            users = res.json()
            if users:
                user_data = pd.DataFrame(users)
                user_data = user_data.rename(columns={
                    "id": "User ID",
                    "name": "Name",
                    "email": "Email",
                    "phone_number": "Phone Number",
                    "date_of_birth": "Date of Birth",
                    "city": "City",
                    "state": "State",
                    "country": "Country"
                })
                st.dataframe(user_data)
            else:
                st.info("No users found.")
        else:
            st.warning(res.json().get("detail", "Failed to fetch users."))
    except Exception as e:
        st.error(f"Error fetching users: {e}")

    # Section 2: View All Accounts
    st.subheader("💳 All Bank Accounts")
    account_data = pd.DataFrame()
    try:
        res = requests.get(f"{BASE_URL}/account/all")
        if res.status_code == 200:
            accounts = res.json()
            if accounts:
                account_data = pd.DataFrame(accounts)
                account_data = account_data.rename(columns={
                    "account_number": "Account Number",
                    "user_id": "User ID",
                    "account_type": "Account Type",
                    "account_balance": "Balance",
                    "created_at": "Created At",
                    "account_status": "Status"
                })
                st.dataframe(account_data)
            else:
                st.info("No accounts found.")
        else:
            st.warning(res.json().get("detail", "Failed to fetch accounts."))
    except Exception as e:
        st.error(f"Error fetching accounts: {e}")

    # Section 3: View All Transactions
    st.subheader("🧾 All Transactions")
    txn_data = pd.DataFrame()
    try:
        res = requests.get(f"{BASE_URL}/transactions/all")
        if res.status_code == 200:
            transactions = res.json()
            if transactions:
                txn_data = pd.DataFrame(transactions)
                txn_data = txn_data.rename(columns={
                    "id": "Transaction ID",
                    "transaction_type": "Transaction Type",
                    "sender_account_id": "Sender Account",
                    "receiver_account_id": "Receiver Account",
                    "amount": "Amount",
                    "remark": "Remark",
                    "transaction_time": "Timestamp",
                    "status": "Status"
                })
                st.dataframe(txn_data)

                # st.markdown("### 📋 Detailed View")
                # for txn in transactions:
                #     with st.expander(f"Txn ID: {txn['id']} | {txn['transaction_type'].capitalize()} ₹{txn['amount']}"):
                #         st.write("🧾 Transaction Type:", txn["transaction_type"].capitalize())
                #         st.write("💰 Amount:", txn["amount"])
                #         st.write("📝 Remark:", txn.get("remark", "N/A"))
                #         st.write("📅 Timestamp:", txn["transaction_time"])
                #         st.write("📤 Sender Account ID:", txn["sender_account_id"])
                #         if txn["receiver_account_id"]:
                #             st.write("📥 Receiver Account ID:", txn["receiver_account_id"])
                #         st.write("📌 Status:", txn.get("status", "N/A"))
            else:
                st.info("No transactions found.")
        else:
            st.warning(res.json().get("detail", "Failed to fetch transactions."))
    except Exception as e:
        st.error(f"Error fetching transactions: {e}")


    # Section 4: Charts & Analytics
    st.subheader("📊 Admin Insights & Platform Analytics")     
            # 1️⃣ Accounts Created Per Month
    st.subheader("📈 Accounts Created Per Month")
    if not account_data.empty:
        try:
            account_data['Created At'] = pd.to_datetime(account_data['Created At'])
            account_data['Month'] = account_data['Created At'].dt.to_period('M').astype(str)
            account_monthly = account_data.groupby('Month').size().reset_index(name='Accounts Created')
            fig1 = px.bar(account_monthly, x='Month', y='Accounts Created',
                        title="📆 Number of Accounts Created Per Month")
            st.plotly_chart(fig1)
        except Exception as e:
            st.warning(f"Failed to plot accounts per month: {e}")
    else:
        st.info("No account data available for monthly chart.")


    # 2️⃣ Total Money Flow Per Transaction Type
    st.subheader("💸 Total Money Flow by Transaction Type")
    try:
        txn_df = pd.DataFrame(transactions)
        if not txn_df.empty:
            txn_summary = txn_df.groupby('transaction_type')['amount'].sum().reset_index()
            fig2 = px.pie(txn_summary, names='transaction_type', values='amount',
                        title='💰 Money Flow Distribution by Transaction Type')
            st.plotly_chart(fig2)
        else:
            st.info("No transactions to visualize.")
    except Exception as e:
        st.warning(f"Failed to plot transaction summary: {e}")


    # 3️⃣ Top N Users by Account Balance
    st.subheader("🏦 Top Users by Account Balance")
    top_n = st.slider("Select number of top users to display", min_value=3, max_value=20, value=5)
    try:
        top_users = account_data.sort_values(by='Balance', ascending=False).head(top_n)
        fig3 = px.bar(top_users, x='User ID', y='Balance',
                    title=f"🏅 Top {top_n} Users by Account Balance",
                    labels={'User ID': 'User ID', 'Balance': 'Account Balance'})
        st.plotly_chart(fig3)
    except Exception as e:
        st.warning(f"Failed to plot top users: {e}")

    st.subheader("📊 Daily Payment Trends")
    txn_df['transaction_time'] = pd.to_datetime(txn_df['transaction_time'])
    txn_df['day'] = txn_df['transaction_time'].dt.to_period('D')
    monthly_trend = txn_df.groupby('day')['amount'].sum().reset_index()
    monthly_trend['day'] = monthly_trend['day'].astype(str)
    st.line_chart(monthly_trend.set_index('day'))


# ----------------account dashboard------------------- #

def account_dashboard():

    st.subheader("📋 What would you like to do?")
    
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔍 View Details"):
            st.session_state.show_section = "view"

    with col2:
        if st.button("💸 Make Transaction"):
            st.session_state.show_section = "transaction"

    with col3:
        if st.button("📜 Transaction History"):
            st.session_state.show_section = "history"

    section = st.session_state.get("show_section", "")
    

    if section == "view":
        show_account_details()
        
    elif section == "transaction":
        make_transaction()
        
    elif section == "history":
        view_transaction_history()
        
    


def show_account_details():
    st.subheader("🔎 Account Details")
    try:
        res = requests.get(f"{BASE_URL}/account/view/{st.session_state.account_number}")
        if res.status_code == 200:
            acc = res.json()
            st.write("**Account Number:**", acc["account_number"])
            st.write("**Type:**", acc["account_type"])
            st.write("**Balance:** Rs. ", acc["account_balance"])
            st.write("**Status:**", acc["account_status"])
            st.write("**Created At:**", acc["created_at"])
        else:
            st.warning(res.json().get("detail", "Could not fetch account details."))
    except Exception as e:
        st.error(f"Error: {e}")

def make_transaction():
    st.subheader("💸 Make a Transaction")

    # Temporary state to track selected transaction type outside the form
    if "txn_type" not in st.session_state:
        st.session_state.txn_type = "Deposit"

    def update_txn_type():
        st.session_state.txn_type = st.session_state.txn_type_selector

    # Transaction type selector (not inside form to allow immediate reaction)
    st.selectbox(
        "Transaction Type",
        ["Deposit", "Withdraw", "Transfer"],
        key="txn_type_selector",
        on_change=update_txn_type
    )

    with st.form("transaction_form"):
        amount = st.number_input("Amount", min_value=10.0)
        remark = st.selectbox("Remark", [
            "travel & ticketing", "food", "clz/school fee", "recharge",
            "rent", "cloth and accessories", "clothes", "other"
        ])

        receiver_acc = None
        if st.session_state.txn_type == "Transfer":
            receiver_acc = st.text_input("Receiver's Account Number")

        txn_submit = st.form_submit_button("Submit Transaction")

    if txn_submit:
        payload = {
            "sender_account_id": st.session_state.account_number,
            "transaction_type": st.session_state.txn_type.lower(),
            "amount": amount,
            "remark": remark,
        }

        if st.session_state.txn_type == "Transfer":
            if not receiver_acc:
                st.warning("Please enter the receiver's account number for a transfer.")
                return
            payload["receiver_account_id"] = receiver_acc

        try:
            res = requests.post(f"{BASE_URL}/transactions/create", json=payload)
            if res.status_code in [200, 201]:
                st.success("✅ Transaction successful!")
            else:
                st.error(res.json().get("detail", "Transaction failed."))
        except Exception as e:
            st.error(f"Error: {e}")



def view_transaction_history():
    st.subheader("📜 Transaction History")
    try:
        res = requests.get(f"{BASE_URL}/transactions/user/{st.session_state.user["user_id"]}")

        if res.status_code == 200:
            transactions = res.json()
            if not transactions:
                st.info("No transactions found.")
            else:
                for txn in transactions:
                    if txn['transaction_type'].lower() == "deposit":
                        st.markdown(f"<span style='color: green;'>**{txn['transaction_type']}**</span> of Rs. {txn['amount']} on {txn['transaction_time']}", unsafe_allow_html=True)
                    elif txn['transaction_type'].lower() == "withdraw":
                        st.markdown(f"<span style='color: red;'>**{txn['transaction_type']}**</span> of Rs. {txn['amount']} on {txn['transaction_time']}", unsafe_allow_html=True)
                    else:
                        st.markdown(f"**{txn['transaction_type']}** of Rs. {txn['amount']} on {txn['transaction_time']}")
        else:
            st.warning(res.json().get("detail", "Could not fetch transaction history."))
    except Exception as e:
        st.error(f"Error fetching history: {e}")
    navigation_footer()


# ------------------- Placeholder for User Dashboard ------------------- #
def user_dashboard():
    st.header("🏦 User Dashboard")

    # 🔐 Step 1: Check if user is logged in
    user = st.session_state.get("user")
    if not user:
        st.error("User session not found. Please log in again.")
        return

    # ✅ Step 2: Check if account exists from backend
    if not st.session_state.get("account_checked", False):
        try:
            res = requests.get(f"{BASE_URL}/account/check/{user['user_id']}")
            if res.status_code == 200:
                account = res.json()
                st.session_state.account_number = account["account_number"]
                st.session_state.account_created = True
            else:
                st.session_state.account_created = False
            st.session_state.account_checked = True
        except Exception as e:
            st.error(f"Error verifying account: {e}")
            return

    # 📝 Step 3: Show "Create Account" form if not created
    if not st.session_state.get("account_created"):
        st.subheader("📝 Create a Bank Account")

        with st.form("create_account_form"):
            account_type = st.selectbox("Account Type", ["Saving", "Current", "Fixed Deposit"])
            initial_balance = st.number_input("Initial Deposit", min_value=0.0, step=100.0)
            create_submit = st.form_submit_button("Create Account")

        if create_submit:
            payload = {
                "user_id": user["user_id"],
                "account_type": account_type,
                "account_status": "Active",
                "account_balance": initial_balance
            }
            try:
                res = requests.post(f"{BASE_URL}/account/create", json=payload)
                if res.status_code in [200, 201]:
                    account = res.json()
                    st.success("✅ Account created successfully!")
                    st.session_state.account_number = account["account_number"]
                    st.session_state.account_created = True
                else:
                    st.error(res.json().get("detail", "Account creation failed."))
            except Exception as e:
                st.error(f"Error: {e}")

    # ✅ Step 4: Account exists — show dashboard
    else:
        st.success("✅ Account already created.")
        account_dashboard()

# ------------------- Main Router ------------------- #
def main():
    st.set_page_config(page_title="Laxmi Bank App", layout="centered")
    st.title("🌻 Laxmi Bank")

    if "page" not in st.session_state:
        st.session_state.page = "home"

    if st.session_state.page == "home":
        st.subheader("Please choose an option")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Register"):
                st.session_state.page = "register"
        with col2:
            if st.button("Login"):
                st.session_state.page = "login"

    elif st.session_state.page == "register":
        register_form()

    elif st.session_state.page == "login":
        login_form()

    elif st.session_state.page == "admin_dashboard":
        admin_dashboard()
        navigation_footer()

    elif st.session_state.page == "user_dashboard":
        user_dashboard()
        navigation_footer()
    elif st.session_state.page == "account_dashboard":
        account_dashboard()
        navigation_footer()

#---------------------Navigation button----------------#
def navigation_footer():
    st.markdown("----")
    col1,col2 = st.columns(2)
    with col1:
        if st.button("Go to Register/Login Page", key="register_login_button"):
            st.session_state.page = "home"
            st.rerun()
    with col2:
        if st.button("🏠Go to Dashboard", key="back_to_dashboard_button"):
            user_data = st.session_state.get("user")
            if user_data.get("is_admin"):
                st.session_state.page = "admin_dashboard"
            else:
                st.session_state.page = "user_dashboard"
            st.rerun()  
           
# ------------------- Run App ------------------- #
if __name__ == "__main__":
    main()
