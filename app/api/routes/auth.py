# # from fastapi import APIRouter, Depends, HTTPException, status
# # from sqlalchemy.orm import Session

# # from app.db.session import get_session
# # from app.api.schemas.auth import UserCreate, UserLogin, TokenResponse
# # from app.services.AuthService import AuthService

# # router = APIRouter(prefix="/auth", tags=["auth"])


# # @router.post(
# #     "/register",
# #     response_model=TokenResponse,
# #     status_code=status.HTTP_201_CREATED,
# # )
# # def register(
# #     request: UserCreate,
# #     session: Session = Depends(get_session),
# # ):
# #     service = AuthService(session)
# #     try:
# #         token = service.register(
# #             username=request.username,
# #             email=request.email,
# #             password=request.password,
# #         )
# #         return {
# #             "access_token": token,
# #             "token_type": "bearer",
# #         }

# #     except ValueError as e:
# #         # Email already registered
# #         raise HTTPException(
# #             status_code=status.HTTP_409_CONFLICT,
# #             detail=str(e),
# #         )


# # @router.post(
# #     "/login",
# #     response_model=TokenResponse,
# # )
# # def login(
# #     request: UserLogin,
# #     session: Session = Depends(get_session),
# # ):
# #     service = AuthService(session)
# #     try:
# #         token = service.login(
# #             email=request.email,
# #             password=request.password,
# #         )
# #         return {
# #             "access_token": token,
# #             "token_type": "bearer",
# #         }

# #     except ValueError:
# #         # Do not leak whether email exists
# #         raise HTTPException(
# #             status_code=status.HTTP_401_UNAUTHORIZED,
# #             detail="Invalid credentials",
# #         )

# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session

# from app.db.session import get_session
# from app.db.models.user import User
# from app.core.security import hash_password, verify_password
# from app.core.jwt import create_access_token

# router = APIRouter(prefix="/auth", tags=["auth"])

# @router.post("/signup")
# def signup(email: str, password: str, session: Session = Depends(get_session)):
#     user = User(
#         email=email,
#         username=email,
#         password_hash=hash_password(password),
#     )
#     session.add(user)
#     session.commit()
#     session.refresh(user)

#     return {"access_token": create_access_token(user.user_id)}

# @router.post("/login")
# def login(email: str, password: str, session: Session = Depends(get_session)):
#     user = session.query(User).filter_by(email=email).one_or_none()
#     if not user or not verify_password(password, user.password_hash):
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     return {"access_token": create_access_token(user.user_id)}

# app/schemas/auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.db.models.user import User
from app.core.security import hash_password, verify_password
from app.core.jwt import create_access_token
from app.schemas.auth import SignupRequest, AuthResponse

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post(
    "/signup",
    response_model=AuthResponse,
    summary="Create a new user account",
    description="Register a new user and return a JWT access token.",
)
def signup(
    payload: SignupRequest,
    session: Session = Depends(get_session),
):
    user = User(
        email=payload.email,
        username=payload.email,
        password_hash=hash_password(payload.password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    return {"access_token": create_access_token(user.user_id)}

@router.post(
    "/login",
    response_model=AuthResponse,
    summary="Login",
    description="Authenticate a user and return a JWT access token.",
)
def login(
    payload: SignupRequest,
    session: Session = Depends(get_session),
):
    user = session.query(User).filter_by(email=payload.email).one_or_none()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"access_token": create_access_token(user.user_id)}
