from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import numpy as np

@dataclass
class Chunk:
    chunk_id: str
    source: str
    text: str

def chunk_text(text: str, source: str, size: int = 180, overlap: int = 30) -> list[Chunk]:
    words = text.split()
    step = max(1, size - overlap)
    chunks: list[Chunk] = []
    for start in range(0, len(words), step):
        part = words[start:start + size]
        if not part:
            break
        chunks.append(Chunk(f"{Path(source).name}:{start // step}", source, " ".join(part)))
        if start + size >= len(words):
            break
    return chunks

def load_documents(folder: str, size: int, overlap: int) -> list[Chunk]:
    chunks: list[Chunk] = []
    for path in sorted(Path(folder).rglob("*")):
        if path.is_file() and path.suffix.lower() in {".md", ".txt"}:
            chunks.extend(chunk_text(path.read_text(encoding="utf-8", errors="ignore"), str(path), size, overlap))
    return chunks

class HybridRetriever:
    def __init__(self, chunks: list[Chunk], embedding_model: str, device: str = "cpu") -> None:
        from sentence_transformers import SentenceTransformer
        from rank_bm25 import BM25Okapi
        if not chunks:
            raise ValueError("No document chunks found")
        self.chunks = chunks
        self.model = SentenceTransformer(embedding_model, device=device)
        self.embeddings = np.asarray(self.model.encode([c.text for c in chunks], normalize_embeddings=True, batch_size=32, show_progress_bar=False), dtype=np.float32)
        self.bm25 = BM25Okapi([self._tokens(c.text) for c in chunks])

    @staticmethod
    def _tokens(text: str) -> list[str]:
        return re.findall(r"[a-z0-9_./:-]+", text.lower())

    def retrieve(self, query: str, dense_k: int, bm25_k: int, final_k: int):
        q = np.asarray(self.model.encode([query], normalize_embeddings=True, show_progress_bar=False)[0], dtype=np.float32)
        dense_ids = np.argsort(-(self.embeddings @ q))[:dense_k]
        lexical_ids = np.argsort(-np.asarray(self.bm25.get_scores(self._tokens(query))))[:bm25_k]
        fused: dict[int, float] = {}
        for rank, idx in enumerate(dense_ids, 1):
            fused[int(idx)] = fused.get(int(idx), 0.0) + 1 / (60 + rank)
        for rank, idx in enumerate(lexical_ids, 1):
            fused[int(idx)] = fused.get(int(idx), 0.0) + 1 / (60 + rank)
        return [(self.chunks[idx], score) for idx, score in sorted(fused.items(), key=lambda x: x[1], reverse=True)[:final_k]]

def build_context(results) -> str:
    return "\n\n".join(f"[source_{i}] {chunk.chunk_id} | {chunk.source}\n{chunk.text}" for i, (chunk, _) in enumerate(results, 1))
