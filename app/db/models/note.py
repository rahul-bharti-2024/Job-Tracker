# app/db/models/note.py
from sqlalchemy import Column, Integer, Text, TIMESTAMP
from sqlalchemy.sql import func
from app.db.models.base import Base

class Note(Base):
    __tablename__ = "notes"

    note_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    application_id = Column(Integer)
    company_id = Column(Integer)
    content = Column(Text, nullable=False)
    created_at = Column(
        TIMESTAMP, server_default=func.now(), nullable=False
    )

