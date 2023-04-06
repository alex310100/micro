from fastapi import FastAPI, HTTPException
from typing import List


class User:
    def __init__(self, id: int, title: str, value: str) -> None:
        self.id = id
        self.title = title
        self.value = value

users: List[User] = [
    User(0, 'First doc', 'qaqaqaqa'),
    User(1,'Second', 'dfvdssdfdgfgdfg')
]

app = FastAPI()

@app.get("/v1/users")
async def get_docs():
    return users #массив

@app.get("/v1/users/{id}")
async def get_docs_by_id(id: int):
    result = [i for i in users if i.id == id]
    if len(result) > 0:
        return result[0]
    raise HTTPException(status_code=404, detail="Document not found")