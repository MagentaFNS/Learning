# fastapi/project_regist/src/main.py
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Session
from datetime import timedelta
import sys
import os
import uvicorn
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Добавляем путь к корневой папке
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

# Импорты из ваших файлов
from database.database import engine, SessionLocal
from database.models import Base, UserDB
from auth import (
    get_current_user,
    get_password_hash,
    authenticate_user,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_db
)


app = FastAPI(
    title="Verification with Project",
    version="1.0.0.0",
    description="API для регистрации и авторизации пользователей с JWT"
)

# --- Pydantic модели ---

class UserCreate(BaseModel):
    """Модель для регистрации нового пользователя"""
    name: str
    age: int
    email: str  # Автоматическая валидация email
    password: str
    return_password: str

    @field_validator('email')
    @classmethod
    def email_verification(cls, v):
        """Валидация email (дополнительная к EmailStr)"""
        if "@" not in v:
            raise ValueError("The mail is incorrect, add '@'.")
        return v

    @field_validator('return_password')
    @classmethod
    def password_verification(cls, v, info):
        """Проверка совпадения паролей"""
        if v != info.data.get('password'):
            raise ValueError("Passwords don't match")
        return v

    @field_validator('password')
    @classmethod
    def password_strength(cls, v):
        """Дополнительная проверка: пароль должен быть длиной минимум 6 символов"""
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return v

class UserResponse(BaseModel):
    """Модель для ответа (без пароля)"""
    id: int
    name: str
    age: int
    email: str
    
    class Config:
        from_attributes = True  # Для работы с SQLAlchemy моделями

class UserLogin(BaseModel):
    """Модель для логина"""
    username: str  # Используем name как username
    password: str

class Token(BaseModel):
    """Модель для JWT токена"""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Данные внутри токена"""
    username: str | None = None

class UserUpdate(BaseModel):
    """Модель для обновления пользователя"""
    name: str | None = None
    age: int | None = None
    email: str | None = None
    password: str | None = None

# --- Эндпоинты ---

@app.post("/register", response_model=UserResponse, tags=['Authentication'])
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Регистрация нового пользователя
    """
    # Проверка уникальности имени
    existing_user = db.query(UserDB).filter(UserDB.username == user.name).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Проверка уникальности email
    existing_email = db.query(UserDB).filter(UserDB.email == user.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Создание нового пользователя
    hashed_password = get_password_hash(user.password)
    db_user = UserDB(
        username=user.name,
        email=user.email,
        hashed_password=hashed_password,
        age=user.age  # Добавляем возраст
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return UserResponse(
        id=db_user.id,
        name=db_user.username,
        age=db_user.age,
        email=db_user.email
    )

@app.post("/login", response_model=Token, tags=['Authentication'])
def login(user: UserLogin, db: Session = Depends(get_db)):
    """
    Логин пользователя с получением JWT токена
    """
    authenticated_user = authenticate_user(db, user.username, user.password)
    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": authenticated_user.username},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

# Альтернативный вариант логина через OAuth2 (стандарт)
@app.post("/token", response_model=Token, tags=['Authentication'])
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Логин через OAuth2 форму (стандартный способ для FastAPI)
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=UserResponse, tags=['Users'])
def get_current_user_info(current_user: UserDB = Depends(get_current_user)):
    """
    Получение информации о текущем авторизованном пользователе
    """
    return UserResponse(
        id=current_user.id,
        name=current_user.username,
        age=current_user.age,
        email=current_user.email
    )

@app.get("/users", response_model=list[UserResponse], tags=['Users'])
def get_all_users(
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """
    Получение списка всех пользователей (только для авторизованных)
    """
    users = db.query(UserDB).all()
    return [
        UserResponse(
            id=user.id,
            name=user.username,
            age=user.age,
            email=user.email
        )
        for user in users
    ]

@app.put("/users/{user_id}", response_model=UserResponse, tags=['Users'])
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """
    Обновление данных пользователя (только для авторизованных)
    """
    # Проверяем, что пользователь обновляет себя
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own profile"
        )
    
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Обновляем поля
    if user_update.name is not None:
        # Проверяем уникальность нового имени
        existing_user = db.query(UserDB).filter(
            UserDB.username == user_update.name,
            UserDB.id != user_id
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        db_user.username = user_update.name
    
    if user_update.age is not None:
        db_user.age = user_update.age
    
    if user_update.email is not None:
        # Проверяем уникальность нового email
        existing_email = db.query(UserDB).filter(
            UserDB.email == user_update.email,
            UserDB.id != user_id
        ).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        db_user.email = user_update.email
    
    if user_update.password is not None:
        if len(user_update.password) < 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 6 characters long"
            )
        db_user.hashed_password = get_password_hash(user_update.password)
    
    db.commit()
    db.refresh(db_user)
    
    return UserResponse(
        id=db_user.id,
        name=db_user.username,
        age=db_user.age,
        email=db_user.email
    )

@app.delete("/users/{user_id}", tags=['Users'])
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """
    Удаление пользователя (только для авторизованных)
    """
    # Проверяем, что пользователь удаляет себя
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own account"
        )
    
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    db.delete(db_user)
    db.commit()
    
    return {"message": f"User {db_user.username} was deleted successfully."}

@app.get("/health", tags=['System'])
def health_check():
    """
    Проверка работоспособности API
    """
    return {"status": "ok", "message": "API is running"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)