# routers/vacancies.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from db import crud, get_db, verify_token
from schemas import VacancyCreate, VacancyOut, VacancyUpdate
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(
    prefix="/vacancy",
    tags=["vacancies"]
)
oauth2_scheme = HTTPBearer()


# Получение списка вакансий
@router.get("/list", response_model=List[VacancyOut])
def read_vacancies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_vacancies(db, skip=skip, limit=limit)


# Создание вакансии (только team_lead_hr)
@router.post("/create", response_model=VacancyOut)
def create_vacancy(vacancy: VacancyCreate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_info = verify_token(token.credentials)
    user_id = user_info["id"]
    if user_info["role"] != "team_lead_hr" and user_info["role"] != "admin":
        print(f"Unauthorized role: {user_info['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create vacancies")

    return crud.create_vacancy(db, title=vacancy.title, description=vacancy.description, user_id=user_id)


# Обновление вакансии (только team_lead_hr)
@router.put("/update/{vacancy_id}", response_model=VacancyOut)
def update_vacancy(vacancy_id: int, vacancy: VacancyUpdate, db: Session = Depends(get_db),
                   token: str = Depends(oauth2_scheme)):
    user_info = verify_token(token.credentials)
    if user_info["role"] != "team_lead_hr" and user_info["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update vacancies")
    return crud.update_vacancy(db, vacancy_id=vacancy_id, vacancy=vacancy)


# Удаление вакансии (только team_lead_hr)
@router.delete("/delete/{vacancy_id}")
def delete_vacancy(vacancy_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user_info = verify_token(token.credentials)
    if user_info["role"] != "team_lead_hr" and user_info["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete vacancies")
    crud.delete_vacancy(db, vacancy_id=vacancy_id)
    return {"detail": "Vacancy deleted"}
