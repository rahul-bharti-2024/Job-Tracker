from sqlalchemy.orm import Session
from app.db.models.application_tag import ApplicationTag
from app.db.models.tag import Tag

class ApplicationTagRepository:
    def __init__(self, session: Session):
        self.session = session

    def attach(self, application_id: int, tag_id: int):
        link = ApplicationTag(
            application_id=application_id,
            tag_id=tag_id,
        )
        self.session.add(link)

    def detach(self, application_id: int, tag_id: int):
        (
            self.session.query(ApplicationTag)
            .filter_by(application_id=application_id, tag_id=tag_id)
            .delete()
        )

    def list_tags(self, application_id: int) -> list[Tag]:
        return (
            self.session.query(Tag)
            .join(ApplicationTag, ApplicationTag.tag_id == Tag.tag_id)
            .filter(ApplicationTag.application_id == application_id)
            .all()
        )
