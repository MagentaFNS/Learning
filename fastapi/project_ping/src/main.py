from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI(
    title="Welcome to backend",
    version="0.0.1"
)

class ItemBase(BaseModel):
    name:str

class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id:int
    name:str

items = []

@app.get("/ping",tags=['Ping'])
def ping():
    return {'status':'ok'}

@app.get("/hello/{name}",tags=['Welcome'])
def welcome(name:str):
    if name.isdigit():
        raise HTTPException(status_code=404,detail='There is no such name, these are numbers.')
    return {"message": f"Hello, {name}"}

@app.get("/items",tags=['Items'])
def items_bd():
    if not items:
        raise HTTPException(status_code=404,detail="Bd is Empty")
    return [{"id": idx, **item} for idx, item in enumerate(items)]

@app.post("/items",tags=['Items'])
def get_items(item:ItemCreate):
    items.append(item.model_dump())
    return {"message":f"Item {item.name} has been added."}

@app.put("/items/{item_id}",tags=['Items'])
def update_items(item_id:int,new_name:ItemCreate):
    if item_id < 0 or item_id >= len(items):
            raise HTTPException(status_code=404,detail='Item not found')
    items[item_id] = new_name.model_dump()
    return {"message":f"Item has been replaced"}

@app.delete("/items/{item_id}",tags=['Items'])
def delete_items(item_id:int):
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404,detail='Item not found')
    item_pop = items.pop(item_id)
    return {"message":f"Item {item_pop} was delete."}

if __name__ == "__main__":
    uvicorn.run("main:app",host='127.0.0.1',port=8000, reload=True)