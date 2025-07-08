from fastapi import APIRouter, HTTPException
from server.services.auth_service import AuthService
from server.config.logging_config import news_agg_logger
from server.models.auth_models import LoginRequest, SignupRequest

router = APIRouter(prefix="/auth", tags=["Auth"])
auth_service = AuthService()


@router.post("/login")
def login(payload: LoginRequest):
    try:
        news_agg_logger(20, f"Login attempt for {payload.email}")
        user = auth_service.login(payload.email, payload.password)
        return user
    except Exception as e:
        news_agg_logger(40, f"Login failed for {payload.email}: {e}")
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/signup")
def signup(payload: SignupRequest):
    try:
        user = auth_service.signup(payload.username, payload.email, payload.password)
        news_agg_logger(20, f"Signup successful for {payload.email}")
        return user
    except Exception as e:
        news_agg_logger(40, f"Signup failed for {payload.email}: {e}")
        raise HTTPException(status_code=400, detail=str(e))
