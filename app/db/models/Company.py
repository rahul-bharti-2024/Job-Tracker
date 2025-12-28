# app/db/models/company.py
from sqlalchemy import Column, Integer, Text, TIMESTAMP
from sqlalchemy.sql import func
from app.db.models.base import Base

class Company(Base):
    __tablename__ = "companies"

    company_id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    website_url = Column(Text)
    location = Column(Text)
    industry = Column(Text)
    created_at = Column(
        TIMESTAMP, server_default=func.now(), nullable=False
    )
