from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class Note(Base):
    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(Integer, ForeignKey("problem.id"), nullable=False)
    content = Column(Text, nullable=False) # The markdown content
    revision_count = Column(Integer, default=0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    problem = relationship("Problem", backref="notes")
