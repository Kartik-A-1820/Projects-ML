from fastapi import FastAPI
from pydantic import BaseModel,Field
from .generator import generate
class Req(BaseModel):
    label:str
    n:int=Field(default=5,ge=1,le=100)
app=FastAPI(title="DataSynth-LLM",version="1.0.0")
@app.get("/health")
def health():return {"status":"ok"}
@app.post("/generate")
def gen(r:Req):return generate(r.label,r.n)
