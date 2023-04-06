from fastapi import FastAPI, HTTPException
from typing import List

class Document:
    def __init__(self, id: int, title: str, value: str) -> None:
        self.id = id
        self.title = title
        self.value = value

documents: List[Document] = [
    Document(0, 'First doc', 'rtgdrtgrdtg'),
    Document(1,'Second', 'dfvdssdfdgfgdfg')
]

app = FastAPI()


@app.get("/v1/docs")
async def get_docs():
    return documents #массив

@app.get("/v1/docs/{id}")
async def get_docs_by_id(id: int):
    result = [i for i in documents if i.id == id]
    if len(result) > 0:
        return result[0]
    raise HTTPException(status_code=404, detail="Document not found")
