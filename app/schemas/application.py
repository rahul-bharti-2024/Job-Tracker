# app/schemas/application.py
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List

from app.schemas.common import ApplicationStatus, ApplicationSource


class ApplicationCreate(BaseModel):
    company_id: int
    role_title: str
    source: ApplicationSource
    applied_date: Optional[date] = None
    deadline_date: Optional[date] = None
    resume_version_id: Optional[int] = None
    tag_ids: List[int] = []


class ApplicationUpdate(BaseModel):
    role_title: Optional[str] = None
    source: Optional[ApplicationSource] = None
    deadline_date: Optional[date] = None
    resume_version_id: Optional[int] = None


class ApplicationResponse(BaseModel):
    application_id: int
    company_id: int
    role_title: str
    source: ApplicationSource
    current_status: ApplicationStatus
    applied_date: Optional[date]
    deadline_date: Optional[date]
    resume_version_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

