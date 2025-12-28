# app/db/models/application_tag.py
from sqlalchemy import Column, Integer
from app.db.models.base import Base

class ApplicationTag(Base):
    __tablename__ = "application_tags"

    application_id = Column(Integer, primary_key=True)
    tag_id = Column(Integer, primary_key=True)

