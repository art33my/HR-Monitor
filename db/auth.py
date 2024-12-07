# db/auth.py

from fastapi import HTTPException, Request
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()  # Загружает переменные из .env

# Конфигурация JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Функция для верификации пароля
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Функция для создания токена доступа
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    print(f"Creating token with data: {data}")  # Логирование данных
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    to_encode["role"] = data.get("role")  # Добавляем роль
    to_encode["id"] = data.get("id")
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(f"Generated token: {encoded_jwt}")  # Логирование токена
    return encoded_jwt


# Функция для верификации токена
def verify_token(token: str):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        print(f"Verifying token: {token}")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        id: int = payload.get("id")
        # Логирование: если роль отсутствует
        if username is None or role is None:
            print(f"Invalid token payload: {payload}")
            raise credentials_exception

        return {"username": username, "role": role, "id": id}
    except JWTError as e:
        print(f"JWTError: {str(e)}")
        raise credentials_exception
