from __future__ import annotations
from pathlib import Path
import yaml
from fastapi import FastAPI
from pydantic import BaseModel
from .core import HybridRetriever, build_context, load_documents
from .generator import LocalGenerator

class QueryRequest(BaseModel):
    question: str

class RAGService:
    def __init__(self, config_path: str = "configs/config.yaml") -> None:
        self.config = yaml.safe_load(Path(config_path).read_text(encoding="utf-8"))
        chunks = load_documents("data/docs", int(self.config["chunk_size_words"]), int(self.config["chunk_overlap_words"]))
        self.retriever = HybridRetriever(chunks, self.config["embedding_model"], device="cpu")
        self.generator: LocalGenerator | None = None

    def _get_generator(self) -> LocalGenerator:
        if self.generator is None:
            self.generator = LocalGenerator(self.config["generator_model"], self.config.get("device", "auto"))
        return self.generator

    def query(self, question: str) -> dict:
        results = self.retriever.retrieve(question, int(self.config["dense_top_k"]), int(self.config["bm25_top_k"]), int(self.config["final_top_k"]))
        answer = self._get_generator().answer(question, build_context(results), int(self.config["max_new_tokens"]))
        return {"answer": answer, "sources": [{"chunk_id": c.chunk_id, "source": c.source, "fusion_score": round(score, 6)} for c, score in results]}

app = FastAPI(title="LocalDoc-RAG", version="1.0.0")
_service: RAGService | None = None

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/query")
def query(request: QueryRequest):
    global _service
    if _service is None:
        _service = RAGService()
    return _service.query(request.question)
