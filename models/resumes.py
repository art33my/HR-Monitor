# models/resumes.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime


class Resume(Base):
    __tablename__ = 'resumes'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    vacancy_id = Column(Integer, ForeignKey('vacancies.id'))
    content = Column(Text)
    source = Column(String)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="resumes")
    vacancy = relationship("Vacancy", back_populates="resumes")
    sla = relationship("SLA", back_populates="resume")
    resume_stages = relationship("ResumeStage", back_populates="resume")
    violations = relationship("SLAViolation", back_populates="resume")

    def __repr__(self):
        return f"<Resume(user_id={self.user_id}, vacancy_id={self.vacancy_id}, status={self.status})>"
