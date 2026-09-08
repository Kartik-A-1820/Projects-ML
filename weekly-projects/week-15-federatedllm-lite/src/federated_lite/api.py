from pathlib import Path
import yaml
from fastapi import FastAPI
from pydantic import BaseModel, Field
from .orchestrator import run_simulation

class SimulationRequest(BaseModel):
    rounds: int = Field(default=2, ge=1, le=10)
    privacy_enabled: bool = True

app = FastAPI(title="FederatedLLM-Lite", version="1.0.0")
CFG = yaml.safe_load(Path("configs/config.yaml").read_text(encoding="utf-8"))

@app.get("/health")
def health(): return {"status":"ok"}

@app.post("/simulate")
def simulate(req: SimulationRequest):
    return run_simulation(CFG, rounds_override=req.rounds, privacy_override=req.privacy_enabled)
