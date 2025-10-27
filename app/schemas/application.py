#apps/schemas/application.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .status import StatusRead
from .source import SourceRead
from .tag import TagRead
from .update import UpdateRead

class ApplicationBase(BaseModel):
    company_name: str
    position_title: str
    job_link: Optional[str] = None
    job_id: Optional[str] = None
    date_applied: Optional[datetime] = None
    source_id: Optional[int] = None
    status_id: Optional[int] = None
    notes: Optional[str] = None

class ApplicationCreate(ApplicationBase):
    tag_ids: Optional[List[int]] = []

class ApplicationUpdate(BaseModel):
    company_name: Optional[str] = None
    position_title: Optional[str] = None
    job_link: Optional[str] = None
    job_id: Optional[str] = None
    status_id: Optional[int] = None
    source_id: Optional[int] = None
    notes: Optional[str] = None
    tag_ids: Optional[List[int]] = []

class ApplicationRead(ApplicationBase):
    id: int
    user_id: int
    status: Optional[StatusRead]
    source: Optional[SourceRead]
    tags: List[TagRead] = []
    updates: List[UpdateRead] = []

    class Config:
        orm_mode = True
