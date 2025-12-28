# app/db/models/status_history.py
from sqlalchemy import Column, Integer, Text, TIMESTAMP
from sqlalchemy.sql import func
from app.db.models.base import Base

class StatusHistory(Base):
    __tablename__ = "status_history"

    id = Column(Integer, primary_key=True)
    application_id = Column(Integer, nullable=False)
    status = Column(Text, nullable=False)
    changed_at = Column(
        TIMESTAMP, server_default=func.now(), nullable=False
    )
