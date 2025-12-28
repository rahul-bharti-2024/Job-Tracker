# app/db/repositories/status_history.py
from sqlalchemy.orm import Session
from app.db.models.status_history import StatusHistory

class StatusHistoryRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, application_id: int, status: str):
        history = StatusHistory(
            application_id=application_id,
            status=status,
        )
        self.session.add(history)
