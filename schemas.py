# schemas.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# Модели для пользователей
class UserCreate(BaseModel):
    username: str
    password: str
    role: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    username: str
    role: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None


class UserDelete(BaseModel):
    id: int


# Модели для вакансий
class VacancyBase(BaseModel):
    title: str
    description: str


class VacancyCreate(VacancyBase):
    pass


class VacancyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class VacancyOut(VacancyBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# Модели для резюме
class ResumeCreate(BaseModel):
    user_id: int
    vacancy_id: int
    content: str
    source: str
    status: str


# Модель для возвращаемого токена
class Token(BaseModel):
    access_token: str
    token_type: str
