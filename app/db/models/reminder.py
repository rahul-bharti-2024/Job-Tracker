# app/db/models/reminder.py
from sqlalchemy import Column, Integer, Text, TIMESTAMP, Boolean
from sqlalchemy.sql import func
from app.db.models.base import Base

class Reminder(Base):
    __tablename__ = "reminders"

    reminder_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    application_id = Column(Integer, nullable=False)
    type = Column(Text, nullable=False)
    scheduled_time = Column(TIMESTAMP, nullable=False)
    message = Column(Text, nullable=False)
    sent = Column(Boolean, nullable=False, server_default="false")

