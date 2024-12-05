# routers/users.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import crud, get_db
from schemas import UserCreate


router = APIRouter()

@router.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, username=user.username, password=user.password, role=user.role)
