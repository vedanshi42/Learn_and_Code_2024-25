from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from server.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])
auth_service = AuthService()


class LoginRequest(BaseModel):
    email: str
    password: str


class SignupRequest(BaseModel):
    username: str
    email: str
    password: str


@router.post("/login")
def login(payload: LoginRequest):
    print(f"Login attempt for {payload.email}")
    user = auth_service.login(payload.email, payload.password)
    if user:
        return user
    raise HTTPException(status_code=401, detail="Invalid credentials")


@router.post("/signup")
def signup(payload: SignupRequest):
    try:
        user_id = auth_service.signup(payload.username, payload.email, payload.password)
        return {"status": "success", "user_id": user_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
