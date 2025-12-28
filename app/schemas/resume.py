# app/schemas/resume.py
from pydantic import BaseModel, HttpUrl
from datetime import datetime

class ResumeCreate(BaseModel):
    external_link: HttpUrl
    version_name: str


class ResumeResponse(BaseModel):
    resume_version_id: int
    external_link: HttpUrl
    version_name: str
    uploaded_at: datetime

    class Config:
        from_attributes = True

