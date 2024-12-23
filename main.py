# main.py
from fastapi import FastAPI
from routers import users, vacancies, resumes, sla, stages, statistic   # Импортируем роутеры

app = FastAPI()

# Подключаем роутеры к приложению через include_router
app.include_router(users.router)
app.include_router(vacancies.router)
app.include_router(resumes.router)
app.include_router(sla.router)
app.include_router(stages.router)
app.include_router(statistic.router)
