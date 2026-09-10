from fastapi import FastAPI
from pydantic import BaseModel,Field
from .core import load_rows,MarginalGainRouter,ModelRouter
class Req(BaseModel):
    query:str=Field(min_length=2);max_cost:float=8.0;max_latency_ms:int=1400
r=ModelRouter(learned=MarginalGainRouter().fit(load_rows()));app=FastAPI(title="ModelRouter-Local")
@app.get("/health")
def health():return {"status":"ok"}
@app.post("/route")
def route(x:Req):return r.route(x.query,max_cost=x.max_cost,max_latency_ms=x.max_latency_ms).__dict__
