# models/sla_violations.py

from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from db.database import Base

class SLAViolation(Base):
    __tablename__ = 'sla_violations'

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey('resumes.id'), nullable=False)
    stage_id = Column(Integer, ForeignKey('stages.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    violation_time = Column(DateTime, default=datetime.utcnow)
    expected_duration = Column(Integer)  # Ожидаемая длительность в часах
    actual_duration = Column(Integer)  # Фактическая длительность в часах

    resume = relationship("Resume", back_populates="violations")
    stage = relationship("Stage", back_populates="violations")
    user = relationship("User", back_populates="violations")
