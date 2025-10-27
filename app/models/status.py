#apps/models/status.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base

class Status(Base):
    __tablename__ = "statuses"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    applications = relationship("Application", back_populates="status")

# Represents job application stages 
# (e.g. Applied, Interviewing, Rejected, Offer).

# One status → many applications.