# app/schemas/status.py
from pydantic import BaseModel
from app.schemas.common import ApplicationStatus

class StatusChangeRequest(BaseModel):
    new_status: ApplicationStatus
