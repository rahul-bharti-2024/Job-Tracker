from sqlalchemy.orm import Session
from app.db.models.User import User
class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, user_id: int) -> User | None:
        return (
            self.session.query(User)
            .filter(User.user_id == user_id)
            .one_or_none()
        )

    def create(self, user: User) -> User:
        self.session.add(user)
        self.session.flush()
        return user

    def list_all(self, limit: int = 100, offset: int = 0) -> list[User]:
        return (
            self.session.query(User)
            .limit(limit)
            .offset(offset)
            .all()
        )

    def delete(self, user_id: int) -> None:
        self.session.query(User).filter(
            User.user_id == user_id
        ).delete()
