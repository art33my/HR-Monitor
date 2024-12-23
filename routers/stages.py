# stages/resumes.py

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
    prefix="/stage",
    tags=["stages"]
)
oauth2_scheme = HTTPBearer()

# Создание стадии
@router.post("/create")
def create_stage(new_stage: StageCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user_info = verify_token(token.credentials)
    if user_info["role"] != "team_lead_hr" and user_info["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update vacancies")
    return crud.create_stage(db, name=new_stage.name, description=new_stage.description)

# Получение стадий
@router.get("/list")
def read_stages(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_stages(db, skip=skip, limit=limit)
