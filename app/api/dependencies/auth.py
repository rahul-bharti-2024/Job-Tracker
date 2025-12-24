from fastapi import Depends, HTTPException
# from fastapi.security import OAuth2PasswordBearer
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()


from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.db.session import get_session
from app.db.models.User import User
from app.core.security import SECRET_KEY, ALGORITHM

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session),
) -> User:
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except (JWTError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid token")

    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
