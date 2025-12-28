# app/db/models/job_application.py
from sqlalchemy import (
    Column,
    Integer,
    Text,
    TIMESTAMP,
    DATE,
    UniqueConstraint,
)
from sqlalchemy.sql import func
from app.db.models.base import Base

class JobApplication(Base):
    __tablename__ = "job_applications"

    application_id = Column(Integer, primary_key=True)

    user_id = Column(Integer, nullable=False)
    company_id = Column(Integer, nullable=False)

    role_title = Column(Text, nullable=False)
    source = Column(Text, nullable=False)
    current_status = Column(Text, nullable=False)

    applied_date = Column(DATE)
    deadline_date = Column(DATE)

    resume_version_id = Column(Integer)

    created_at = Column(
        TIMESTAMP, server_default=func.now(), nullable=False
    )
    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "company_id",
            "role_title",
            name="uq_user_company_role",
        ),
    )
