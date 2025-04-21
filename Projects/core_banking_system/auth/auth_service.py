from user.user_schema import User
from database import MySQLConnection

def authenticate_user(email: str, password: str):
    session = MySQLConnection.SessionLocal()
    user = session.query(User).filter_by(email= email, password= password).first()
    session.close()
    return user