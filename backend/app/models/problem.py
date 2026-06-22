from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.db.base_class import Base

class Problem(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    url = Column(String, unique=True, index=True, nullable=False)
    difficulty = Column(String, index=True)
    topic = Column(String, index=True)
    tags = Column(String) # Stored as comma-separated or JSON string for simplicity initially
    statement = Column(Text)
    constraints = Column(Text)
    examples = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
