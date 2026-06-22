from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NoteBase(BaseModel):
    content: str
    revision_count: int = 0

class NoteCreate(NoteBase):
    problem_id: int

class NoteUpdate(NoteBase):
    content: Optional[str] = None
    revision_count: Optional[int] = None

class NoteInDBBase(NoteBase):
    id: int
    problem_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Note(NoteInDBBase):
    pass
