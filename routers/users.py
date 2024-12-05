# routers/users.py

from fastapi import APIRouter, Depends, HTTPException, status, FastAPI
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from db import crud, get_db, create_access_token, verify_password, verify_token
from schemas import UserCreate, UserLogin, Token, UserOut
from models import User
from typing import List

router = APIRouter(
    prefix="/users",
    tags=["users"]
)
oauth2_scheme = HTTPBearer()


# Авторизация
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    access_token = create_access_token(data={"sub": db_user.username, "role": db_user.role})
    return {"access_token": access_token, "token_type": "bearer"}


# Получение информации о пользователе
@router.get("/me", response_model=UserOut)
def get_current_user_info(token: HTTPAuthorizationCredentials = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    token_value = token.credentials
    user_info = verify_token(token_value)
    username = user_info["username"]
    if not username:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
    db_user = db.query(User).filter(User.username == username).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# Создание пользователя (только admin)
@router.post("/create_user")
def create_user(new_user: UserCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user_info = verify_token(token.credentials)
    if user_info["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create users")
    return crud.create_user(db=db, username=new_user.username, password=new_user.password, role=new_user.role)


# Получение списка пользователей (только admin)
@router.get("/")
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user_info = verify_token(token.credentials)
    if user_info["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to read users")
    return crud.get_users(db, skip=skip, limit=limit)


# Удаление пользователя (только admin)
@router.delete("/delete/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user_info = verify_token(token.credentials)
    if user_info["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete users")
    crud.delete_user(db, user_id=user_id)
    return {"detail": "User deleted"}
