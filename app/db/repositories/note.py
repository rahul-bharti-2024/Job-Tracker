from sqlalchemy.orm import Session
from app.db.models.note import Note


class NoteRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(
        self,
        *,
        user_id: int,
        content: str,
        application_id: int | None = None,
        company_id: int | None = None,
    ) -> Note:
        note = Note(
            user_id=user_id,
            content=content,
            application_id=application_id,
            company_id=company_id,
        )
        self.session.add(note)
        return note

    def list_for_application(self, application_id: int) -> list[Note]:
        return (
            self.session.query(Note)
            .filter(Note.application_id == application_id)
            .order_by(Note.created_at.desc())
            .all()
        )

