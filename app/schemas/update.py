#apps/schemas/update.py

from pydantic import BaseModel
from datetime import datetime

class UpdateBase(BaseModel):
    update_text: str

class UpdateCreate(UpdateBase):
    pass

class UpdateRead(UpdateBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
