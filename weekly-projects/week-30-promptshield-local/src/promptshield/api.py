from fastapi import FastAPI
from pydantic import BaseModel
from .policy import PolicyEngine
from .gateway import SecureToolGateway
from .audit import AuditLog
import os
class ToolRequest(BaseModel):
    session_id:str; objective:str; tool:str; args:dict; observation:str=""; approved:bool=False
policy=PolicyEngine(os.getenv("PROMPTSHIELD_POLICY","configs/policy.yaml"))
gateway=SecureToolGateway(policy,AuditLog(os.getenv("PROMPTSHIELD_AUDIT_PATH","artifacts/audit.jsonl")))
app=FastAPI(title="PromptShield-Local",version="1.0.0")
@app.get("/health")
def health(): return {"status":"ok"}
@app.post("/authorize")
def authorize(req:ToolRequest): return gateway.request(**req.model_dump())
