from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.db.repositories.job_application import JobApplicationRepository
from app.db.models.job_application import JobApplication
class ApplicationReadService:
    def __init__(self, session: Session):
        self.repo = JobApplicationRepository(session)

    def get_application(
        self,
        *,
        application_id: int,
        user_id: int,
    ) -> JobApplication:
        app = self.repo.get_by_id(application_id)
        if not app or app.user_id != user_id:
            raise HTTPException(status_code=404, detail="Application not found")
        return app

    def list_applications(self, user_id: int) -> list[JobApplication]:
        return self.repo.list_by_user(user_id)

    def list_applications_filtered(
        self,
        *,
        user_id: int,
        status: str | None = None,
        tag: str | None = None,
    ):
        if status:
            return self.repo.list_by_user_and_status(user_id, status)

        if tag:
            return self.repo.list_by_user_and_tag(user_id, tag)

        return self.repo.list_by_user(user_id)
