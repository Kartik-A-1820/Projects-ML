# Week 01 — LocalDoc-RAG (2026 Rebuild)

A current hybrid local RAG implementation for Ryzen 7 4800-series, 16 GB RAM and GTX 1650 Ti 4 GB.

## Stack
- MiniLM dense retrieval on CPU
- BM25 lexical retrieval
- Reciprocal Rank Fusion
- Qwen2.5-1.5B-Instruct generation on GPU
- FastAPI
- citation-aware answers

## Run
```bash
pip install -r requirements.txt
python run.py "Why is hybrid retrieval useful?"
```

API: `uvicorn localdoc_rag.app:app --app-dir src --host 127.0.0.1 --port 8000`

Tests: `pytest -q`

## Resume bullet
Built a local-first hybrid RAG platform combining dense retrieval, BM25 and reciprocal-rank fusion with citation-aware local SLM generation, optimized for 4 GB VRAM and designed for distributed production retrieval and inference.
