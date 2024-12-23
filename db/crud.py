# db/crud.py

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
import bcrypt
from models import User, Vacancy, Resume, Stage, ResumeStage, SLA, SLAViolation
from schemas import VacancyUpdate, UserUpdate, ResumeUpdate
from datetime import datetime, timedelta



# Функции для работы с пользователями

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()  # Генерируем соль
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)  # Хешируем пароль
    return hashed.decode('utf-8')  # Преобразуем в строку для хранения в БД


def create_user(db: Session, username: str, password: str, role: str):
    hashed_password = hash_password(password)  # Хешируем пароль
    db_user = User(username=username, password=hashed_password, role=role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()


def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Vacancy not found")

    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user


# Функции для работы с вакансиями
def create_vacancy(db: Session, title: str, description: str, user_id: int):
    db_vacancy = Vacancy(title=title, description=description, user_id=user_id)
    db.add(db_vacancy)
    db.commit()
    db.refresh(db_vacancy)
    return db_vacancy


def get_vacancies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Vacancy).offset(skip).limit(limit).all()


def update_vacancy(db: Session, vacancy_id: int, vacancy: VacancyUpdate):
    db_vacancy = db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
    if not db_vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")

    for key, value in vacancy.dict(exclude_unset=True).items():
        setattr(db_vacancy, key, value)

    db.commit()
    db.refresh(db_vacancy)
    return db_vacancy


def delete_vacancy(db: Session, vacancy_id: int):
    db_vacancy = db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
    if not db_vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")

    db.delete(db_vacancy)
    db.commit()


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

def delete_resume(db: Session, resume_id: int):
    db_resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not db_resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    db.delete(db_resume)
    db.commit()

def update_resume(db: Session, resume_id: int, resume: ResumeUpdate):
    db_resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not db_resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    for key, value in resume.dict(exclude_unset=True).items():
        setattr(db_resume, key, value)

    db.commit()
    db.refresh(db_resume)
    return db_resume
# Функции для работы с стадиями

def create_stage(db: Session, name: str, description: str):
    db_stage = Stage(name=name, description=description)
    db.add(db_stage)
    db.commit()
    db.refresh(db_stage)
    return db_stage


def get_stages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Stage).offset(skip).limit(limit).all()


def move_resume_to_stage(db: Session, resume_id: int, stage_id: int):
    # Получаем текущую стадию резюме
    current_stage = db.query(ResumeStage).filter(
        ResumeStage.resume_id == resume_id, ResumeStage.ended_at.is_(None)
    ).first()

    if current_stage:
        current_stage.ended_at = datetime.utcnow()
        db.add(current_stage)
        db.commit()

        # Проверка на нарушение SLA
        sla = db.query(SLA).filter(SLA.resume_id == resume_id, SLA.stage_id == stage_id).first()
        if sla:
            # Вычисляем время, которое резюме провело на стадии
            time_spent = current_stage.ended_at - current_stage.started_at
            expected_duration = timedelta(hours=sla.duration)

            # Если время превышает ожидания по SLA
            if time_spent > expected_duration:
                violation = SLAViolation(
                    resume_id=resume_id,
                    stage_id=stage_id,
                    user_id=current_stage.resume.user_id,
                    violation_time=datetime.utcnow(),
                    expected_duration=int(expected_duration.total_seconds() // 3600),  # Время в часах
                    actual_duration=int(time_spent.total_seconds() // 3600)  # Время в часах
                )
                db.add(violation)
                db.commit()

    # Добавляем новую стадию
    new_stage = ResumeStage(
        resume_id=resume_id,
        stage_id=stage_id,
        started_at=datetime.utcnow()
    )
    db.add(new_stage)

    # Обновляем статус в таблице resumes
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if resume:
        stage = db.query(Stage).filter(Stage.id == stage_id).first()
        if stage:
            resume.status = stage.name
            db.add(resume)

    db.commit()
    db.refresh(new_stage)
    return new_stage

# Функции для работы с SLA
def create_sla(db: Session, resume_id: int, stage_id: int, duration: float):
    db_sla = SLA(resume_id=resume_id, stage_id=stage_id, duration=duration)
    db.add(db_sla)
    db.commit()
    db.refresh(db_sla)
    return db_sla

def get_sla_violations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(SLAViolation).offset(skip).limit(limit).all()

# Функции для работы со статистикой

def get_average_time_per_stage(db: Session, user_id: int = None):
    query = db.query(
        ResumeStage.stage_id,
        func.avg(func.extract('epoch', ResumeStage.ended_at - ResumeStage.started_at)).label('average_time')
    ).join(Resume).filter(ResumeStage.ended_at.isnot(None))

    if user_id:
        query = query.filter(Resume.user_id == user_id)

    return query.group_by(ResumeStage.stage_id).all()

def get_resumes_distribution_by_stage(db: Session, user_id: int = None):
    query = db.query(
        Resume.status,
        func.count(Resume.id).label('count')
    )
    if user_id:
        query = query.filter(Resume.user_id == user_id)

    return query.group_by(Resume.status).all()

def get_resumes_distribution_by_source(db: Session, user_id: int = None):
    query = db.query(
        Resume.source,
        func.count(Resume.id).label('count')
    )
    if user_id:
        query = query.filter(Resume.user_id == user_id)

    return query.group_by(Resume.source).all()

def get_average_candidates_per_vacancy(db: Session):
    subquery = db.query(
        Resume.vacancy_id,
        func.count(Resume.id).label('candidate_count')
    ).group_by(Resume.vacancy_id).subquery()

    return db.query(func.avg(subquery.c.candidate_count)).scalar()

def get_sla_violations_count(db: Session, user_id: int = None):
    query = db.query(
        SLAViolation.stage_id,
        func.count(SLAViolation.id).label('violation_count')
    )
    if user_id:
        query = query.filter(SLAViolation.user_id == user_id)

    return query.group_by(SLAViolation.stage_id).all()
