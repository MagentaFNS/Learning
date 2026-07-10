from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

class Item(BaseModel):
    name:str = "Нет информации"

items = ["task1","task2"]

app = FastAPI()

@app.get('/root')
async def ping():
    return {'message':'ok'}

@app.post("/Items")
def post(item:Item):
    items.append(item.name)
    return {"message":f"Добавлено: {item.name}"}

@app.put("/items/{item_id}")
def put(item_id:int,new_item:Item):
    items[item_id] = new_item
    return {"message":f"Предмет под индексом {item_id} был обновлен на {new_item}"}

@app.delete("/item/{item_id}")
def delete(item_id:int):
    items.pop(item_id)
    return {"message":f"Предмет под индексом {item_id} был удален"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)