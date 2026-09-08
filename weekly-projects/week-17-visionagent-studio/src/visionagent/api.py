from fastapi import FastAPI
from pydantic import BaseModel,Field
from .tools import ToolRegistry,detect_objects,read_text,spatial_relation
from .agent import VisionAgent
class Req(BaseModel):
    scene:dict
    query:str=Field(min_length=2)
reg=ToolRegistry();reg.register("objects",detect_objects);reg.register("ocr",read_text);reg.register("spatial",spatial_relation)
agent=VisionAgent(reg)
app=FastAPI(title="VisionAgent-Studio",version="1.0.0")
@app.get("/health")
def health():return {"status":"ok"}
@app.post("/reason")
def reason(r:Req):return agent.run(r.scene,r.query)
