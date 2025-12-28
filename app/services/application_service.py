from sqlalchemy.orm import Session

from app.db.models.job_application import JobApplication
from app.db.repositories.job_application import JobApplicationRepository
from app.db.repositories.status_history import StatusHistoryRepository
from app.schemas.application import ApplicationCreate
from app.schemas.common import ApplicationStatus


class ApplicationService:
    def __init__(self, session: Session):
        self.session = session
        self.app_repo = JobApplicationRepository(session)
        self.history_repo = StatusHistoryRepository(session)

    def create_application(self, *, user_id: int, data: ApplicationCreate):
        app = JobApplication(
            user_id=user_id,
            company_id=data.company_id,
            role_title=data.role_title,
            source=data.source.value,
            current_status=ApplicationStatus.SAVED.value,
            applied_date=data.applied_date,
            deadline_date=data.deadline_date,
            resume_version_id=data.resume_version_id,
        )

        self.app_repo.create(app)
        self.session.flush()  # assigns application_id

        self.history_repo.create(
            application_id=app.application_id,
            status=ApplicationStatus.SAVED.value,
        )

        self.session.commit()
        self.session.refresh(app)
        return app

