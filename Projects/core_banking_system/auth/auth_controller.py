from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from auth.auth_service import authenticate_user

auth_router = APIRouter()

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@auth_router.post("/login")
def login(login_data: LoginRequest):
    user = authenticate_user(login_data.email, login_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {"message": "Login successful", "user_id": user.id, "is_admin": user.is_admin}