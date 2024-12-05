# models/vacancies.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime


class Vacancy(Base):
    __tablename__ = 'vacancies'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Связь с резюме
    resumes = relationship("Resume", back_populates="vacancy")

    def __repr__(self):
        return f"<Vacancy(title={self.title}, created_at={self.created_at})>"
