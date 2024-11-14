# models/stages.py
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from database import Base

class Stage(Base):
    __tablename__ = 'stages'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)

    resume_stages = relationship("ResumeStage", back_populates="stage")  # связь с resume_stages
    sla = relationship("SLA", back_populates="stage")  # связь с SLA

    def __repr__(self):
        return f"<Stage(name={self.name}, description={self.description})>"
