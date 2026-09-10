from fastapi import FastAPI
from pydantic import BaseModel,Field
from .core import HybridEngine
class Req(BaseModel):
    query:str=Field(min_length=2);top_k:int=5;fusion:str="rrf"
e=HybridEngine();app=FastAPI(title="HybridSearch-RAG")
@app.get("/health")
def health():return {"status":"ok"}
@app.post("/search")
def search(r:Req):return e.search(r.query,r.top_k,r.fusion)
