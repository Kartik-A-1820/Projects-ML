from pathlib import Path
from fastapi import FastAPI,UploadFile,File
from PIL import Image
import io,json
from .index import ExemplarIndex
from .engine import VisionRAG

app=FastAPI(title="VisionRAG-Local",version="1.0.0")
_engine=None

def engine():
    global _engine
    if _engine is None:
        _engine=VisionRAG(ExemplarIndex.build("data/manifest.json"))
    return _engine

@app.get("/health")
def health():return {"status":"ok"}

@app.post("/predict")
async def predict(file:UploadFile=File(...)):
    image=Image.open(io.BytesIO(await file.read())).convert("RGB")
    return engine().predict(image)
