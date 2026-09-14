from fastapi import FastAPI
from pydantic import BaseModel,Field
import numpy as np
from .pipeline import EdgeVisionPipeline

class Frame(BaseModel):
    frame_id:int
    pixels:list[list[float]]
    size:int=Field(default=256,ge=32,le=1024)

app=FastAPI(title='EdgeVision-Analytics',version='1.0.0')
pipeline=EdgeVisionPipeline(frame_stride=1)

@app.get('/health')
def health(): return {'status':'ok'}

@app.post('/inspect')
def inspect(frame:Frame):
    arr=np.asarray(frame.pixels,dtype='float32')
    return pipeline.process(frame.frame_id,arr)
