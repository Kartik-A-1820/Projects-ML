from fastapi import FastAPI
from pydantic import BaseModel,Field
from .engine import GraphRAG
class Query(BaseModel):
    query:str=Field(min_length=2)
    top_k:int=Field(default=5,ge=1,le=20)
app=FastAPI(title="GraphRAG-Enterprise",version="1.0.0")
engine=GraphRAG()
@app.get("/health")
def health():return {"status":"ok"}
@app.post("/search")
def search(q:Query):return engine.search(q.query,q.top_k)
