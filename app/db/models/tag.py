# app/db/models/tag.py
from sqlalchemy import Column, Integer, Text
from app.db.models.base import Base

class Tag(Base):
    __tablename__ = "tags"

    tag_id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)

