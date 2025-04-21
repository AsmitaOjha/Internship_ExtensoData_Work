from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from user.user_schema import UserCreate, UserOut
from user.user_service import create_user, get_user_by_email, get_all_users
from sqlalchemy.exc import IntegrityError
from fastapi import status


user_router = APIRouter()

@user_router.post("/register", response_model=UserOut)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = create_user(user_data, db)
        return new_user

    except IntegrityError as e:
        # Likely a duplicate email or unique constraint violation
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists. Please use a different email."
        )

    except ValueError as ve:
        # If your create_user function validates and raises ValueError
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(ve)
        )

    except Exception as e:
        # Generic fallback for unexpected issues
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An unexpected error occurred while registering. Please try again later."
        )

@user_router.get("/exists")
def check_user_exists(email: str, db: Session = Depends(get_db)):
    user = get_user_by_email(db, email)
    return {"exists": bool(user)}

@user_router.get("/all")
def get_all_user(db: Session = Depends(get_db)):
    users = get_all_users(db)
    return users;