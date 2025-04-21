from user.user_schema import User, UserCreate
from sqlalchemy.orm import Session

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(user_data: UserCreate, db: Session):
    new_user = User(
        name=user_data.name,
        date_of_birth=user_data.date_of_birth,
        gender=user_data.gender,
        phone_number=user_data.phone_number,
        email=user_data.email,
        password=user_data.password,
        city=user_data.city,
        state=user_data.state,
        country=user_data.country,
        is_admin=user_data.is_admin if user_data.is_admin is not None else False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_all_users(db: Session):
    return db.query(User).all();