# app/db/repositories/job_application.py
from sqlalchemy.orm import Session
from app.db.models.job_application import JobApplication

from app.db.models.application_tag import ApplicationTag
from app.db.models.tag import Tag

#session -> 
class JobApplicationRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, application_id: int) -> JobApplication | None:
        return (
            self.session
            .query(JobApplication)
            .filter_by(application_id=application_id)
            .one_or_none()
        )

    def update_status(self, application: JobApplication, new_status: str):
        application.current_status = new_status
        self.session.add(application)

    def create(self, application: JobApplication):
        self.session.add(application)

    def list_by_user(self, user_id:int)-> list[JobApplication]:
        return (
            self.session
            .query(JobApplication)
            .filter_by(user_id=user_id)
            .order_by(JobApplication.updated_at.desc())
            .all()
        )
    def list_by_user_and_status(self, user_id: int, status: str):
        return (
            self.session.query(JobApplication)
            .filter(
                JobApplication.user_id == user_id,
                JobApplication.current_status == status,
            )
            .order_by(JobApplication.updated_at.desc())
            .all()
        )
    
    def list_by_user_and_tag(self, user_id: int, tag_name: str):
        return (
            self.session.query(JobApplication)
            .join(
                ApplicationTag,
                ApplicationTag.application_id == JobApplication.application_id,
            )
            .join(
                Tag,
                Tag.tag_id == ApplicationTag.tag_id,
            )
            .filter(
                JobApplication.user_id == user_id,
                Tag.name == tag_name,
            )
            .order_by(JobApplication.updated_at.desc())
            .all()
        )