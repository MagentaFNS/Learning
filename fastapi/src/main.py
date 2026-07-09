from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

@app.get('/root')
async def ping():
    return {'message':'ok'}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)