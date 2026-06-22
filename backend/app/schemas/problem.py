from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class ProblemBase(BaseModel):
    title: str
    url: str
    difficulty: Optional[str] = None
    topic: Optional[str] = None
    tags: Optional[str] = None
    statement: Optional[str] = None
    constraints: Optional[str] = None
    examples: Optional[str] = None

class ProblemCreate(ProblemBase):
    pass

class ProblemUpdate(ProblemBase):
    title: Optional[str] = None
    url: Optional[str] = None

class ProblemInDBBase(ProblemBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Problem(ProblemInDBBase):
    pass
