from sqlalchemy import Column, BigInteger, Text, TIMESTAMP
from sqlalchemy.sql import func
from .base import Base

class Company(Base):
    __tablename__ = "companies"

    company_id = Column(BigInteger, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    website_url = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
