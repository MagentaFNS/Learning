from fastapi import FastAPI,Depends,HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import sys
import os
import uvicorn

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from database.bd import SessionLocal, engine
from database.models import Base, ItemDB

Base.metadata.create_all(bind=engine)

app = FastAPI()

class ItemsCreate(BaseModel):
    name:str

class ItemResponse(BaseModel):
    id:int
    name: str

def get_bd():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/root')
async def ping():
    return {'message':'ok'}

#для просмотра списка

@app.get("/items",response_model=list[ItemResponse])
def get_items(db: Session = Depends(get_bd)):
    items = db.query(ItemDB).all()
    return items

#Добовление в список

@app.post("/Items",response_model=ItemResponse)
def create_item(item:ItemsCreate, db: Session = Depends(get_bd)):
    item_db = ItemDB(name = item.name)
    db.add(item_db)
    db.commit()
    db.refresh(item_db)
    return item_db

#Обновление списка

@app.put("/items/{item_id}",response_model=ItemResponse)
def update_item(item_id:int,item:ItemsCreate,db: Session = Depends(get_bd)):
    db_item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404,detail='Items not found')
    
    db_item.name = item.name
    db.commit()
    db.refresh(db_item)
    return db_item

#удаление элемента

@app.delete("/items/{item_id}")
def delete_item(item_id:int,db: Session = Depends(get_bd)):
    db_item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404,detail="Item not found")

    db.delete(db_item)
    db.commit()
    return {"message":f"Item с id {item_id} удалён"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)