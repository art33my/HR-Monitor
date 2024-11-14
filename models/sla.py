# models/sla.py
from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from database import Base

class SLA(Base):
    __tablename__ = 'sla'

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey('resumes.id'))
    stage_id = Column(Integer, ForeignKey('stages.id'))
    duration = Column(Float)

    resume = relationship("Resume", back_populates="sla")
    stage = relationship("Stage", back_populates="sla")

    def __repr__(self):
        return f"<SLA(resume_id={self.resume_id}, stage_id={self.stage_id}, duration={self.duration})>"
