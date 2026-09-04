from fastapi import FastAPI
from pydantic import BaseModel,Field
from .engine import Engine
app=FastAPI(title='MultiPDF-RAG',version='1.0.0'); engine=Engine(['data/policies.txt','data/platform.txt'])
class Q(BaseModel): query:str=Field(min_length=1); top_k:int=Field(default=5,ge=1,le=20)
@app.get('/health')
def health(): return {'status':'ok'}
@app.post('/query')
def query(q:Q): return engine.query(q.query,q.top_k)
