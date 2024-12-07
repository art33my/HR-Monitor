# models/users.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from db.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Связь с резюме
    resumes = relationship("Resume", back_populates="user")

    # Связь с Vacancy
    vacancies = relationship("Vacancy", back_populates="user")

    def __repr__(self):
        return f"<User(username={self.username}, role={self.role})>"
