# routers/vacancies.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import crud, get_db
from schemas import VacancyCreate


router = APIRouter()

@router.post("/vacancies/")
def create_vacancy(vacancy: VacancyCreate, db: Session = Depends(get_db)):
    return crud.create_vacancy(db=db, title=vacancy.title, description=vacancy.description)
