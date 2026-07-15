from fastapi import FastAPI,HTTPException,Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import sys
import os
import uvicorn

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from database.bd import SessionLocal,engine
from database.models import ItemDB, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Memoria Core API",
    description="Безопасное ядро для хранения и управления текстовыми сущностями. Memoria Core обеспечивает высокоскоростной доступ к данным, поддерживая полнотекстовый поиск, версионирование и гибкую систему тегов. Ваша цифровая память, защищенная на уровне базы данных.",
    version="1.0.0"
)

class ItemsCreate(BaseModel):
    name:str

class ItemResponse(BaseModel):
    id:int
    name:str

def get_bd():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/",response_model=list[ItemResponse],tags=["Tasks"])
def task(db: Session = Depends(get_bd)):
    items = db.query(ItemDB).all()
    return items

@app.post("/append_task",response_model=ItemResponse,tags=["Tasks"])
def append_task(item:ItemsCreate,db: Session = Depends(get_bd)):
    item_db = ItemDB(name = item.name)
    db.add(item_db)
    db.commit()
    db.refresh(item_db)
    return item_db

@app.put("/put_task",response_model=ItemResponse,tags=["Tasks"])
def put_task(item_id:int,new_item:ItemsCreate,db: Session = Depends(get_bd)):
    db_item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404,detail='Items not found')
    db_item.name = new_item.name
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/delete_task",tags=["Tasks"])
def delete_task(item_id:int,db: Session = Depends(get_bd)):
    db_item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404,detail=f"Индекс {item_id} не был найден.")
    db.delete(db_item)
    db.commit()
    return {"message":f"Item с id {item_id} удалён"}

if __name__ == "__main__":
    uvicorn.run("main:app",host="127.0.0.1", port=8000,reload = True)