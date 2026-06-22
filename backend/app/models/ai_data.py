from sqlalchemy import Column, Integer, String, JSON, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base

class ProblemAnalysis(Base):
    __tablename__ = "problem_analysis"
    
    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(Integer, ForeignKey("problem.id"), unique=True, index=True)
    data = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    problem = relationship("Problem", back_populates="analysis")

class ProblemSolution(Base):
    __tablename__ = "problem_solution"
    
    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(Integer, ForeignKey("problem.id"), unique=True, index=True)
    data = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    problem = relationship("Problem", back_populates="solution")

class ProblemReview(Base):
    __tablename__ = "problem_review"
    
    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(Integer, ForeignKey("problem.id"), unique=True, index=True)
    data = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    problem = relationship("Problem", back_populates="review")

class ProblemNotes(Base):
    __tablename__ = "problem_notes"
    
    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(Integer, ForeignKey("problem.id"), unique=True, index=True)
    teacher_data = Column(JSON, nullable=True)
    similarity_data = Column(JSON, nullable=True)
    markdown_content = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    problem = relationship("Problem", back_populates="notes")
