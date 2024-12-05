# schemas.py
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    role: str

class VacancyCreate(BaseModel):
    title: str
    description: str

class ResumeCreate(BaseModel):
    user_id: int
    vacancy_id: int
    content: str
    source: str
    status: str