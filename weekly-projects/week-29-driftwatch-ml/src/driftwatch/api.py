from fastapi import FastAPI
from pydantic import BaseModel
from .monitor import DriftMonitor

class Payload(BaseModel):
    reference:dict[str,list[float]]
    current:dict[str,list[float]]

app=FastAPI(title='DriftWatch-ML',version='1.0.0')
monitor=DriftMonitor()

@app.get('/health')
def health():return {'status':'ok'}

@app.post('/inspect')
def inspect(p:Payload):
    return [r.__dict__ for r in monitor.inspect(p.reference,p.current)]
