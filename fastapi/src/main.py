from fastapi import FastAPI,HTTPException,APIRouter
from pydantic import BaseModel
import uvicorn

class items(BaseModel):
    name:str

app = FastAPI(
    title="Memoria Core API",
    description="Безопасное ядро для хранения и управления текстовыми сущностями. Memoria Core обеспечивает высокоскоростной доступ к данным, поддерживая полнотекстовый поиск, версионирование и гибкую систему тегов. Ваша цифровая память, защищенная на уровне базы данных.",
    version="1.0.0"
)

tasks = []


@app.get("/",tags=["Tasks"])
def task():
    return {"message":tasks}

@app.post("/append_task",tags=["Tasks"])
def append_task(item:items):
    tasks.append(item.name)
    return {"message":f"Задача добавлена: {item.name}"}

@app.put("/put_task",tags=["Tasks"])
def put_task(item_id:int,new_item:items):
    if item_id not in tasks:
        raise HTTPException(status_code=404,detail=f"Индекс {item_id} не был найден.")
    tasks[item_id] = new_item.name
    return {"message":f"Задача индекса: {item_id}, обновленна на {new_item}"}

@app.delete("/delete_task",tags=["Tasks"])
def delete_task(item_id:int):
    if item_id not in tasks:
        raise HTTPException(status_code=404,detail=f"Индекс {item_id} не был найден.")
    tasks.pop(item_id)
    return {"message":f"Задача индекса: {item_id},была удалена"}

if __name__ == "__main__":
    uvicorn.run("main:app",host="127.0.0.1", port=8000,reload = True)