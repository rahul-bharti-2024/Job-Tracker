from pydantic  import BaseModel
from typing import Optional, List
from datetime import date

class CreateApplicationRequest(BaseModel):

    company_id: int
    external_job_id: str
    job_posting_url: Optional[str] = None
    role_title: Optional[str] = None
    status: str
    date_applied: Optional[date] = None
    expected_next_action_date: Optional[date] = None

class UpdateApplicationRequest(BaseModel):
    status: Optional[str] = None
    expected_next_action_date: Optional[date] = None