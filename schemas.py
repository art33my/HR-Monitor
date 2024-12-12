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
    user_id: int

    class Config:
        orm_mode = True


# Модели для резюме
class Resume(BaseModel):
    user_id: int
    vacancy_id: int
    content: str
    source: str
    status: str
    created_at: datetime

class ResumeCreate(BaseModel):
    vacancy_id: int
    content: str
    source: str
    status: str


class ResumeUpdate(BaseModel):
    vacancy_id: Optional[int] = None
    content: Optional[str] = None
    status: Optional[str] = None

# Модель для возвращаемого токена
class Token(BaseModel):
    access_token: str
    token_type: str

class MoveResumeSchema(BaseModel):
    stage_id: int

class ResumeStageSchema(BaseModel):
    id: int
    resume_id: int
    stage_id: int
    started_at: datetime
    ended_at: datetime | None

    class Config:
        orm_mode = True

class StageCreate(BaseModel):
    name: str
    description: str