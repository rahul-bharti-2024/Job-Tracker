from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.api.schemas.auth import UserCreate, UserLogin, TokenResponse
from app.services.AuthService import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=TokenResponse)
def register(
    request: UserCreate,
    session: Session = Depends(get_session),
):
    service = AuthService(session)
    try:
        token = service.register(
            username=request.username,
            email=request.email,
            password=request.password,
        )
        return {"access_token": token}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=TokenResponse)
def login(
    request: UserLogin,
    session: Session = Depends(get_session),
):
    service = AuthService(session)
    try:
        token = service.login(
            email=request.email,
            password=request.password,
        )
        return {"access_token": token}
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid credentials")
