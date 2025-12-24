from sqlalchemy.orm import Session
from app.db.models.User import User
from app.core.security import hash_password, verify_password, create_access_token

class AuthService:
    def __init__(self, session: Session):
        self.session = session

    def register(self, username: str, email: str, password: str) -> str:
        if self.session.query(User).filter_by(email=email).first():
            raise ValueError("Email already registered")

        user = User(
            username=username,
            email=email,
            password_hash=hash_password(password),
        )
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return create_access_token(user.user_id)

    def login(self, email: str, password: str) -> str:
        user = self.session.query(User).filter_by(email=email).first()
        if not user or not verify_password(password, user.password_hash):
            raise ValueError("Invalid credentials")

        return create_access_token(user.user_id)
