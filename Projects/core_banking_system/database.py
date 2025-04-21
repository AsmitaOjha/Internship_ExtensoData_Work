from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

user = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_DATABASE")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")

if not user:
    exit("Please set the environment variable DB_USERNAME")

# Safe encoding of password
DB_URL = f"mysql+pymysql://{user}:{quote_plus(password)}@{db_host}:{db_port}/{db_name}"

# Create engine and session
engine = create_engine(DB_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Class wrapper for structure
class MySQLConnection:
    engine = engine
    SessionLocal = SessionLocal
    Base = Base

def get_db():
    db = MySQLConnection.SessionLocal()
    try:
        yield db
    finally:
        db.close()