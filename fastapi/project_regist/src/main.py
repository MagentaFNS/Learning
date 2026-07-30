# Изучение Валидаторов, регистрация пользователя.
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

app = FastAPI(
    title="Verification",
    version="1.0.0.0"
)

# Временное хранилище (имитация БД)
user_dict = []

class User(BaseModel):
    name: str
    age: int
    email: str
    password: str
    return_password: str

    @field_validator('email')
    @classmethod
    def email_verification(cls, v):
        if "@" not in v:
            raise ValueError("The mail is incorrect, add '@'.")
        return v

    @field_validator('return_password')
    @classmethod
    def password_verification(cls, v, info):
        if v != info.data.get('password'):
            raise ValueError("Passwords don't match")
        return v


@app.get('/users', tags=['List users'])
def get_users():
    return {"users": user_dict}


@app.post("/add_user", tags=['Add user'])
def add_user(user: User):
    user_dict.append(user.model_dump())
    return {"message": f"User {user.name} has been added."}


@app.put("/put_user/{user_id}", tags=['Put user'])
def put_user(user_id: int, new_user: User):
    if user_id < 0 or user_id >= len(user_dict):
        raise HTTPException(status_code=404, detail="User not found")
    user_dict[user_id] = new_user.model_dump()
    return {"message": f"User {new_user.name} has been replaced"}


@app.delete("/delete_user/{user_id}", tags=['Delete user'])
def delete_user(user_id: int):
    if user_id < 0 or user_id >= len(user_dict):
        raise HTTPException(status_code=404, detail="User not found")
    removed = user_dict.pop(user_id)
    return {"message": f"User {removed['name']} was deleted."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)