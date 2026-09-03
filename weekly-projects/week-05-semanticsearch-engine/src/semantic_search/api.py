from fastapi import FastAPI
from pydantic import BaseModel, Field

from .engine import SearchEngine, load_documents


class Query(BaseModel):
    query: str = Field(min_length=1)
    top_k: int = Field(default=5, ge=1, le=50)
    filters: dict | None = None


app = FastAPI(title="SemanticSearch-Engine", version="1.0.0")
_engine = SearchEngine(load_documents("data/documents.json"))


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/search")
def search(payload: Query):
    return [hit.__dict__ for hit in _engine.search(payload.query, payload.top_k, payload.filters)]
