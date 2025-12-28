# app/services/status_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.schemas.common import ApplicationStatus
from app.services.status_rules import ALLOWED_TRANSITIONS
from app.db.repositories.job_application import JobApplicationRepository
from app.db.repositories.status_history import StatusHistoryRepository

class StatusService:
    def __init__(self, session: Session):
        self.session = session
        self.app_repo = JobApplicationRepository(session)
        self.history_repo = StatusHistoryRepository(session)

    def change_status(
        self,
        *,
        application_id: int,
        user_id: int,
        new_status: ApplicationStatus,
    ):
        application = self.app_repo.get_by_id(application_id)

        if not application or application.user_id != user_id:
            raise HTTPException(status_code=404, detail="Application not found")

        current_status = ApplicationStatus(application.current_status)

        allowed = ALLOWED_TRANSITIONS.get(current_status)
        if not allowed:
            raise HTTPException(
                status_code=400,
                detail=f"No transitions defined for status {current_status}",
            )

        if new_status not in allowed:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid transition {current_status} → {new_status}",
            )

        self.app_repo.update_status(application, new_status.value)
        self.history_repo.create(application_id, new_status.value)

        self.session.commit()
