# app/schemas/note.py
from pydantic import BaseModel, model_validator
from typing import Optional
from datetime import datetime

class NoteCreate(BaseModel):
    application_id: Optional[int] = None
    company_id: Optional[int] = None
    content: str

    @model_validator(mode="after")
    def validate_target(self):
        if not self.application_id and not self.company_id:
            raise ValueError("Note must belong to application or company")
        if self.application_id and self.company_id:
            raise ValueError("Note cannot belong to both")
        return self


class NoteResponse(BaseModel):
    note_id: int
    user_id: int
    application_id: Optional[int]
    company_id: Optional[int]
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

