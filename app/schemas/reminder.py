# app/schemas/reminder.py
from pydantic import BaseModel
from datetime import datetime
from app.schemas.common import ReminderType

class ReminderCreate(BaseModel):
    application_id: int
    type: ReminderType
    scheduled_time: datetime
    message: str


class ReminderResponse(BaseModel):
    reminder_id: int
    application_id: int
    type: ReminderType
    scheduled_time: datetime
    message: str
    sent: bool

    class Config:
        from_attributes = True

