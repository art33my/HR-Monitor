# routers/resumes.py

from fastapi import APIRouter, Depends, HTTPException, status, FastAPI
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from db import crud, get_db, create_access_token, verify_password, verify_token
from schemas import UserCreate, UserLogin, Token, UserOut, ResumeCreate, Resume, ResumeUpdate, MoveResumeSchema, ResumeStageSchema, StageCreate
from models import Resume as ResumeModel
from typing import List
from typing import Optional
from fastapi import Query


router = APIRouter(
    prefix="/resume",
    tags=["resumes"]
)
oauth2_scheme = HTTPBearer()

# Получение списка резюме
@router.get("/list", response_model=List[Resume])
def get_resumes(
        skip: int = 0,
        limit: int = 10,
        stage: Optional[str] = Query(None, description="Фильтр по стадии"),
        vacancy_id: Optional[int] = Query(None, description="Фильтр по вакансии"),
        start_date: Optional[str] = Query(None, description="Фильтр по дате начала (YYYY-MM-DD)"),
        end_date: Optional[str] = Query(None, description="Фильтр по дате окончания (YYYY-MM-DD)"),
        db: Session = Depends(get_db),
):
    query = db.query(ResumeModel)

    if stage:
        query = query.filter(ResumeModel.status == stage)
    if vacancy_id:
        query = query.filter(ResumeModel.vacancy_id == vacancy_id)
    if start_date:
        query = query.filter(ResumeModel.created_at >= start_date)
    if end_date:
        query = query.filter(ResumeModel.created_at <= end_date)

    resumes = query.offset(skip).limit(limit).all()
    return resumes


# Создание резюме
@router.post("/create")
def create_resume(new_resume: ResumeCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user_info = verify_token(token.credentials)
    user_id = user_info["id"]
    return crud.create_resume(db, user_id=user_id, vacancy_id=new_resume.vacancy_id, content=new_resume.content, source=new_resume.source, status=new_resume.status)



# Удаление резюме (только team_lead)
@router.delete("/delete/{resume_id}")
def delete_resume(resume_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user_info = verify_token(token.credentials)

    if user_info["role"] != "admin" and user_info["role"] !="team_lead_hr" :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete users")
    crud.delete_resume(db, resume_id=resume_id)
    return {"detail": "Resume deleted"}

# Обновление резюме (только team_lead_hr)
@router.put("/update/{resume_id}")
def update_vacancy(resume_id: int, resume: ResumeUpdate, db: Session = Depends(get_db),
                   token: str = Depends(oauth2_scheme)):
    user_info = verify_token(token.credentials)
    if user_info["role"] != "team_lead_hr" and user_info["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update vacancies")
    return crud.update_resume(db, resume_id=resume_id, resume=resume)

# Перемещение резюме
@router.post("/{resume_id}/move", response_model=ResumeStageSchema)
def move_resume(resume_id: int, move_data: MoveResumeSchema, db: Session = Depends(get_db)):
    new_stage = crud.move_resume_to_stage(db, resume_id, move_data.stage_id)
    if not new_stage:
        raise HTTPException(status_code=404, detail="Resume or Stage not found")
    return new_stage

# Создание стадии
@router.post("/create_stage")
def create_stage(new_stage: StageCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user_info = verify_token(token.credentials)
    if user_info["role"] != "team_lead_hr" and user_info["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update vacancies")
    return crud.create_stage(db, name=new_stage.name, description=new_stage.description)

# Получение стадий
@router.get("/list_stages")
def read_stages(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_stages(db, skip=skip, limit=limit)