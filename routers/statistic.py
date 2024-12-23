# statistic/resumes.py

from fastapi import APIRouter, Depends, HTTPException, status, FastAPI
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from db import crud, get_db, create_access_token, verify_password, verify_token, get_sla_violations
from schemas import (UserCreate, UserLogin, Token, UserOut, ResumeCreate, Resume, ResumeUpdate, MoveResumeSchema,
                     ResumeStageSchema, StageCreate, SLACreate)
from models import Resume as ResumeModel
from models import SLA
from typing import List
from typing import Optional
from fastapi import Query


router = APIRouter(
    prefix="/statistic",
    tags=["statistic"]
)
oauth2_scheme = HTTPBearer()


@router.get("/average-time-per-stage")
def average_time_per_stage(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Получение среднего времени нахождения резюме на каждой стадии.
    """
    user_info = verify_token(token.credentials)
    user_id = user_info["id"]
    user_role = user_info["role"]

    if user_role == "hr":
        return crud.get_average_time_per_stage(db, user_id=user_id)
    elif user_role == "team lead hr":
        return crud.get_average_time_per_stage(db)
    else:
        return {"error": "Access denied"}


@router.get("/resumes-distribution-by-stage")
def resumes_distribution_by_stage(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Получение распределения резюме по стадиям.
    """
    user_info = verify_token(token.credentials)
    user_id = user_info["id"]
    user_role = user_info["role"]

    if user_role == "hr":
        return crud.get_resumes_distribution_by_stage(db, user_id=user_id)
    elif user_role == "team lead hr":
        return crud.get_resumes_distribution_by_stage(db)
    else:
        return {"error": "Access denied"}


@router.get("/resumes-distribution-by-source")
def resumes_distribution_by_source(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Получение распределения резюме по источникам.
    """
    user_info = verify_token(token.credentials)
    user_id = user_info["id"]
    user_role = user_info["role"]

    if user_role == "hr":
        return crud.get_resumes_distribution_by_source(db, user_id=user_id)
    elif user_role == "team lead hr":
        return crud.get_resumes_distribution_by_source(db)
    else:
        return {"error": "Access denied"}


@router.get("/average-candidates-per-vacancy")
def average_candidates_per_vacancy(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Получение среднего количества кандидатов на одну вакансию.
    """
    user_info = verify_token(token.credentials)
    user_role = user_info["role"]

    if user_role == "team lead hr":
        return {"average_candidates": crud.get_average_candidates_per_vacancy(db)}
    else:
        return {"error": "Access denied"}


@router.get("/sla-violations")
def sla_violations(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Получение количества нарушений SLA.
    """
    user_info = verify_token(token.credentials)
    user_id = user_info["id"]
    user_role = user_info["role"]

    if user_role == "hr":
        return crud.get_sla_violations_count(db, user_id=user_id)
    elif user_role == "team lead hr":
        return crud.get_sla_violations_count(db)
    else:
        return {"error": "Access denied"}