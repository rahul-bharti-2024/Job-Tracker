#apps/schemas/source.py
from pydantic import BaseModel

class SourceBase(BaseModel):
    name: str

class SourceCreate(SourceBase):
    pass

class SourceRead(SourceBase):
    id: int
    class Config:
        orm_mode = True
