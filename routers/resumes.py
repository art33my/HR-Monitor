# routers/resumes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import crud, get_db
from schemas import ResumeCreate

router = APIRouter()


@router.post("/resumes/")
def create_resume(resume: ResumeCreate, db: Session = Depends(get_db)):
    return crud.create_resume(
        db=db,
        user_id=resume.user_id,
        vacancy_id=resume.vacancy_id,
        content=resume.content,
        source=resume.source,
        status=resume.status
    )
