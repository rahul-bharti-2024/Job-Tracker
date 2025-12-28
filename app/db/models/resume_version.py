# app/db/models/resume_version.py
from sqlalchemy import Column, Integer, Text, TIMESTAMP
from sqlalchemy.sql import func
from app.db.models.base import Base

class ResumeVersion(Base):
    __tablename__ = "resume_versions"

    resume_version_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    external_link = Column(Text, nullable=False)
    version_name = Column(Text, nullable=False)
    uploaded_at = Column(
        TIMESTAMP, server_default=func.now(), nullable=False
    )
