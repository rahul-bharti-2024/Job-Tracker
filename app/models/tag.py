#apps/models/tag.py
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

# Association Table
application_tags = Table(
    "application_tags",
    Base.metadata,
    Column("application_id", Integer, ForeignKey("applications.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True)
)

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    applications = relationship(
        "Application",
        secondary=application_tags,
        back_populates="tags"
    )

# application_tags is an association table that connects applications and tags.
# It has no id of its own — it’s just a linking table.

# Each tag (e.g., "Frontend", "Remote", "Urgent") can apply to multiple applications.