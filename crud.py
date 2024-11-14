# crud.py
from sqlalchemy.orm import Session
from models import User, Vacancy, Resume, Stage, ResumeStage, SLA

# Функции для работы с пользователями
def create_user(db: Session, username: str, password: str, role: str):
    db_user = User(username=username, password=password, role=role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

# Функции для работы с вакансиями
def create_vacancy(db: Session, title: str, description: str):
    db_vacancy = Vacancy(title=title, description=description)
    db.add(db_vacancy)
    db.commit()
    db.refresh(db_vacancy)
    return db_vacancy

def get_vacancies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Vacancy).offset(skip).limit(limit).all()

# Функции для работы с резюме
def create_resume(db: Session, user_id: int, vacancy_id: int, content: str, source: str, status: str):
    db_user = db.query(User).filter(User.id == user_id).first()
    db_vacancy = db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()

    if not db_user or not db_vacancy:
        raise ValueError("User or Vacancy not found")

    db_resume = Resume(user_id=user_id, vacancy_id=vacancy_id, content=content, source=source, status=status)
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    return db_resume


def get_resumes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Resume).offset(skip).limit(limit).all()

# Функции для работы с стадиями
def create_stage(db: Session, name: str, description: str):
    db_stage = Stage(name=name, description=description)
    db.add(db_stage)
    db.commit()
    db.refresh(db_stage)
    return db_stage

def get_stages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Stage).offset(skip).limit(limit).all()

# Функции для работы с SLA
def create_sla(db: Session, resume_id: int, stage_id: int, duration: float):
    db_sla = SLA(resume_id=resume_id, stage_id=stage_id, duration=duration)
    db.add(db_sla)
    db.commit()
    db.refresh(db_sla)
    return db_sla
