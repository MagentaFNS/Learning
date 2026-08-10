from fastapi import FastAPI,HTTPException,Depends
from fastapi.testclient import TestClient
from pydantic import BaseModel
from sqlalchemy.orm import Session
import os
import sys
import uvicorn

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))

from Python.database.database import SessionLocal
from Python.database.models import ItemDB

app = FastAPI(
    title="Project Riddles API",
    description="API для загадок и не более",
    version="1.0.0"
)

class ItemCreate(BaseModel):
    name:str

class ItemResponse(BaseModel):
    id:int
    name:str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/Riddles",response_model=list[ItemResponse],tags=["Riddles"])
def get(db:Session = Depends(get_db)):
    db_items = db.query(ItemDB).all()
    if len(db_items) == 0:
        raise HTTPException(status_code=404,detail="BD is EMPTY")
    return db_items

@app.post("/Riddles_append",response_model=ItemResponse,tags=["Riddles"])
def append(Item:ItemCreate,db:Session = Depends(get_db)):
    db_items = ItemDB(name = Item.name)
    db.add(db_items)
    db.commit()
    db.refresh(db_items)
    return db_items

@app.put("/Riddles_put",response_model=ItemResponse,tags=["Riddles"])
def put(item_id:int,new_item:ItemCreate,db:Session = Depends(get_db)):
    db_items = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    db_items.name = new_item.name
    db.commit()
    db.refresh(db_items)
    return db_items

@app.delete("/Riddles_delete",response_model=ItemResponse,tags=["Riddles"])
def delete(item_id:int,db:Session = Depends(get_db)):
    db_items = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if db_items is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_items)
    db.commit()
    return db_items

client = TestClient(app)

def test_read_main():
    response = client.get("/Riddles")
    
    # Если БД пуста, то будет 404
    if response.status_code == 404:
        assert response.json()["detail"] == "BD is EMPTY"
        return
    
    # Если БД не пуста
    assert response.status_code == 200
    data = response.json()  # ✅ Исправлено: добавил ()
    
    assert isinstance(data, list)
    
    if len(data) > 0:
        assert "id" in data[0]
        assert "name" in data[0]

def test_create_main():
    # ✅ Исправлено: POST вместо GET
    response = client.post("/Riddles_append", json={"name": "Test Riddle"})
    
    assert response.status_code == 200
    data = response.json()  # ✅ Исправлено: добавил ()
    assert data["name"] == "Test Riddle"
    assert "id" in data

def test_update_item():
    # Создаем элемент
    create_resp = client.post("/Riddles_append", json={"name": "Old Name"})
    assert create_resp.status_code == 200
    item_id = create_resp.json()["id"]
    
    # Обновляем элемент
    update_resp = client.put(
        f"/Riddles_put?item_id={item_id}", 
        json={"name": "New Name"}
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["name"] == "New Name"

def test_delete_item():
    # Создаем элемент
    create_resp = client.post("/Riddles_append", json={"name": "To Delete"})
    assert create_resp.status_code == 200
    item_id = create_resp.json()["id"]
    
    # Удаляем элемент
    delete_resp = client.delete(f"/Riddles_delete?item_id={item_id}")
    assert delete_resp.status_code == 200

# ✅ Добавил тест для проверки ошибок
def test_delete_nonexistent():
    """Проверка удаления несуществующего элемента"""
    response = client.delete("/Riddles_delete?item_id=99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)