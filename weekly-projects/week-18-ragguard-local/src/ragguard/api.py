from fastapi import FastAPI
from pydantic import BaseModel,Field
from .guard import RAGGuard

class Inspect(BaseModel): text:str=Field(min_length=1)
app=FastAPI(title="RAGGuard-Local",version="1.0.0")
guard=RAGGuard()
@app.get("/health")
def health(): return {"status":"ok"}
@app.post("/inspect/input")
def inspect_input(req:Inspect): return guard.inspect_input(req.text)
@app.post("/inspect/output")
def inspect_output(req:Inspect): return guard.inspect_output(req.text)
