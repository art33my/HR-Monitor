# sla/resumes.py

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
    prefix="/sla",
    tags=["sla"]
)
oauth2_scheme = HTTPBearer()

# Указание sla
@router.post("/create", response_model=SLACreate)
def create_sla(sla: SLACreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user_info = verify_token(token.credentials)
    if user_info["role"] != "team_lead_hr" and user_info["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update vacancies")
    # Проверяем, существует ли уже SLA для данного resume_id и stage_id
    existing_sla = db.query(SLA).filter(SLA.resume_id == sla.resume_id, SLA.stage_id == sla.stage_id).first()
    if existing_sla:
        raise HTTPException(status_code=400, detail="SLA for this resume and stage already exists.")

    # Создаем новую запись SLA
    new_sla = SLA(resume_id=sla.resume_id, stage_id=sla.stage_id, duration=sla.duration)
    db.add(new_sla)
    db.commit()
    db.refresh(new_sla)
    return new_sla

# Список нарушений sla
@router.get("/violations/")
def read_sla_violations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user_info = verify_token(token.credentials)
    if user_info["role"] != "team_lead_hr" and user_info["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update vacancies")
    violations = get_sla_violations(db, skip=skip, limit=limit)
    return violations