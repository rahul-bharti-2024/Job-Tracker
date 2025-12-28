from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.db.models.tag import Tag
from app.db.repositories.application_tag import ApplicationTagRepository
from app.db.repositories.job_application import JobApplicationRepository


class TagService:
    def __init__(self, session: Session):
        self.session = session
        self.app_repo = JobApplicationRepository(session)
        self.tag_repo = ApplicationTagRepository(session)

    def _get_application_or_404(self, application_id: int, user_id: int):
        app = self.app_repo.get_by_id(application_id)
        if not app or app.user_id != user_id:
            raise HTTPException(status_code=404, detail="Application not found")
        return app

    def _get_or_create_tag(self, name: str) -> Tag:
        tag = (
            self.session.query(Tag)
            .filter(Tag.name == name)
            .one_or_none()
        )
        if tag:
            return tag

        tag = Tag(name=name)
        self.session.add(tag)
        self.session.flush()
        return tag

    def attach_tag(self, *, application_id: int, user_id: int, tag_name: str):
        self._get_application_or_404(application_id, user_id)
        tag = self._get_or_create_tag(tag_name)

        self.tag_repo.attach(application_id, tag.tag_id)
        self.session.commit()

    def detach_tag(self, *, application_id: int, user_id: int, tag_id: int):
        self._get_application_or_404(application_id, user_id)

        self.tag_repo.detach(application_id, tag_id)
        self.session.commit()

    def list_tags(self, *, application_id: int, user_id: int):
        self._get_application_or_404(application_id, user_id)
        return self.tag_repo.list_tags(application_id)
