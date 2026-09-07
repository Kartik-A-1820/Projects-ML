from fastapi import FastAPI
from pydantic import BaseModel, Field
from .io import load_events
from .retrieval import VideoRetriever, evidence_bundle

class Query(BaseModel):
    query:str=Field(min_length=2)
    top_k:int=Field(default=5,ge=1,le=20)

app=FastAPI(title="VideoRAG-Local",version="1.0.0")
retriever=VideoRetriever(load_events("data/events.json"))

@app.get("/health")
def health(): return {"status":"ok"}

@app.post("/search")
def search(q:Query):
    hits=retriever.search(q.query,q.top_k)
    return {"hits":[h.__dict__ for h in hits],"evidence":evidence_bundle(q.query,hits)}
