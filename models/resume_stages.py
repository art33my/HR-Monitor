# models/resume_stages.py
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class ResumeStage(Base):
    __tablename__ = 'resume_stages'

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey('resumes.id'))
    stage_id = Column(Integer, ForeignKey('stages.id'))
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)

    resume = relationship("Resume", back_populates="resume_stages")  # обратная связь с Resume
    stage = relationship("Stage", back_populates="resume_stages")

    def __repr__(self):
        return f"<ResumeStage(resume_id={self.resume_id}, stage_id={self.stage_id}, started_at={self.started_at})>"

