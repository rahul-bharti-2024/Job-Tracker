from sqlalchemy import (
    Column,
    BigInteger,
    Text,
    TIMESTAMP,
    DATE,
    UniqueConstraint,
)
from sqlalchemy.sql import func
from .base import Base

class JobApplication(Base):
    __tablename__ = "job_applications"

    application_id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, nullable=False)
    company_id = Column(BigInteger, nullable=False)

    external_job_id = Column(Text, nullable=False)
    job_posting_url = Column(Text, nullable=True)
    role_title = Column(Text, nullable=True)

    status = Column(Text, nullable=False)

    date_applied = Column(DATE, nullable=True)
    expected_next_action_date = Column(DATE, nullable=True)

    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
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
            "external_job_id",
            name="uq_user_company_external_job",
        ),
    )
