#apps/models/application.py
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base
from app.models.tag import application_tags

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company_name = Column(String, nullable=False)
    position_title = Column(String, nullable=False)
    job_link = Column(Text)
    job_id = Column(String)
    date_applied = Column(DateTime, default=datetime.utcnow)

    source_id = Column(Integer, ForeignKey("sources.id"))
    status_id = Column(Integer, ForeignKey("statuses.id"))

    notes = Column(Text)

    # Relationships
    user = relationship("User", back_populates="applications")
    status = relationship("Status", back_populates="applications")
    source = relationship("Source", back_populates="applications")
    tags = relationship("Tag", secondary=application_tags, back_populates="applications")
    updates = relationship("Update", back_populates="application", cascade="all, delete")


# Concept: Central table — every application belongs to one user, has one source, one status, multiple tags, and multiple updates.

# Foreign Keys:

# user_id → users.id

# source_id → sources.id

# status_id → statuses.id

# Relationships:

# user gives the linked user object.

# tags uses a secondary (bridge) table for many-to-many (application_tags).

# cascade="all, delete" means if an application is deleted, its updates are too.