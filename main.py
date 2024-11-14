# main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, init_db
import crud

app = FastAPI()

# Инициализация БД и создание всех таблиц
init_db()

# Получение сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Эндпоинт для создания пользователя
@app.post("/users/")
def create_user(username: str, password: str, role: str, db: Session = Depends(get_db)):
    return crud.create_user(db=db, username=username, password=password, role=role)

# Эндпоинт для создания вакансии
@app.post("/vacancies/")
def create_vacancy(title: str, description: str, db: Session = Depends(get_db)):
    return crud.create_vacancy(db=db, title=title, description=description)

# Эндпоинт для создания резюме
@app.post("/resumes/")
def create_resume(user_id: int, vacancy_id: int, content: str, source: str, status: str, db: Session = Depends(get_db)):
    return crud.create_resume(db=db, user_id=user_id, vacancy_id=vacancy_id, content=content, source=source, status=status)
