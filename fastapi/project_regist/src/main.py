#Изучение Валидаторов,регистрация пользователя.
from fastapi import FastAPI,Depends,HTTPException
from pydantic import BaseModel,Field,field_validator
from sqlalchemy.orm import Session
import os
import sys
import uvicorn

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from database.bd import SessionLocal,engine
from database.models import ItemDB,Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Verification",
    version="1.0.0.0"
)

class User(BaseModel):
    name:str
    age:int
    email:str
    password:str
    return_password:str


    @field_validator('email')
    @classmethod
    def email_verification(cls,v):
        if "@" not in v:
            raise ValueError("Тhe mail is incorrect,add '@'.")
        return v
    
    @field_validator('return_password')
    @classmethod
    def password_verification(cls,v,info):
        if v != info.data.get('password'):
            raise ValueError("Passwords don't match")
        return v

user_dict = []

@app.get('/user',tags=['List users'])
def get_user():
    return {'message':user_dict}

@app.post("/add_user",tags=['Add user'])
def add_user(user:User):
    user_dict.append(user)
    return {"message":f"User {user.name} has been added."}

@app.put("/put_user",tags=['Put user'])
def put_user(user_id:int,new_user:User):
    user_dict[user_id] = new_user
    return {"message":f"User {new_user.name} has been replaced"}

@app.delete("/delete_user",tags=['Delete user'])
def delete_user(user_id:int):
    user_dict.pop(user_id)
    return {"message":f"{user_id} was delete."}

if __name__ == "__main__":
    uvicorn.run("main:app",host="127.0.0.1", port=8000,reload = True)