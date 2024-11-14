FROM python:3.11-slim

# Установим зависимости
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY . /app/

# Команда для запуска приложения через uvicorn как модуль
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
