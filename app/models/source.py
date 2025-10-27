#apps/models/source.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base

class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    applications = relationship("Application", back_populates="source")

# Represents where you found the job.
# One source (e.g. "LinkedIn") → many applications.