from fastapi import FastAPI,HTTPException,Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import os
import sys
import uvicorn

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from database.database import SessionLocal,engine
from database.models import Base,ItemDB

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Welcome to backend",
    version="0.0.1"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ItemCreate(BaseModel):
    name:str

class ItemResponse(BaseModel):
    id:int
    name:str

@app.get("/ping",tags=['Ping'])
def ping():
    return {'status':'ok'}

@app.get("/hello/{name}",tags=['Welcome'])
def welcome(name:str):
    if name.isdigit():
        raise HTTPException(status_code=404,detail='There is no such name, these are numbers.')
    return {"message": f"Hello, {name}"}

@app.get("/items",response_model=list[ItemResponse],tags=['Items'])
def items_bd(db:Session = Depends(get_db)):
    db_items = db.query(ItemDB).all()
    if len(db_items) == 0:
        raise HTTPException(status_code=404,detail="Bd is Empty")
    return db_items

@app.post("/items",response_model=ItemResponse,tags=['Items'])
def get_items(item:ItemCreate,db:Session = Depends(get_db)):
    db_items = ItemDB(name = item.name)
    db.add(db_items)
    db.commit()
    db.refresh(db_items)
    return db_items

@app.put("/items/{item_id}",response_model=ItemResponse,tags=['Items'])
def update_items(item_id:int,new_name:ItemCreate,db:Session = Depends(get_db)):
    all_items = db.query(ItemDB).order_by(ItemDB.id).all()
    if item_id < 0 or item_id >= len(all_items):
            raise HTTPException(status_code=404,detail='Item not found')
    db_item = all_items[item_id]
    db_item.name = new_name.name
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/items/{item_id}",tags=['Items'])
def delete_items(item_id:int,db:Session = Depends(get_db)):
    all_items = db.query(ItemDB).order_by(ItemDB.id).all()
    if item_id < 0 or item_id >= len(all_items):
        raise HTTPException(status_code=404,detail='Item not found')
    db_item = all_items[item_id]
    db.delete(db_item)
    db.commit()
    return {"message":f"Item {db_item.id} was delete."}

if __name__ == "__main__":
    uvicorn.run("main:app",host='127.0.0.1',port=8000, reload=True)