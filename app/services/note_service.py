from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.repositories.note import NoteRepository
from app.db.repositories.job_application import JobApplicationRepository
from app.db.models.note import Note


class NoteService:
    def __init__(self, session: Session):
        self.session = session
        self.note_repo = NoteRepository(session)
        self.app_repo = JobApplicationRepository(session)

    def add_note_to_application(
        self,
        *,
        user_id: int,
        application_id: int,
        content: str,
    ) -> Note:
        app = self.app_repo.get_by_id(application_id)
        if not app or app.user_id != user_id:
            raise HTTPException(status_code=404, detail="Application not found")

        note = self.note_repo.create(
            user_id=user_id,
            content=content,
            application_id=application_id,
        )
        self.session.commit()
        self.session.refresh(note)
        return note

    def list_application_notes(
        self,
        *,
        user_id: int,
        application_id: int,
    ) -> list[Note]:
        app = self.app_repo.get_by_id(application_id)
        if not app or app.user_id != user_id:
            raise HTTPException(status_code=404, detail="Application not found")

        return self.note_repo.list_for_application(application_id)

