# Week 01 — LocalDoc-RAG
A current hybrid local RAG implementation for Ryzen 7 4800-series, 16 GB RAM and GTX 1650 Ti 4 GB.
## Stack
- MiniLM dense retrieval on CPU
- BM25 lexical retrieval
- Reciprocal Rank Fusion
- Qwen2.5-1.5B-Instruct generation on GPU
- FastAPI
- citation-aware answers
Run commands from this lab's directory in an activated, isolated environment. See the [setup and contribution guide](../../CONTRIBUTING.md) before starting.
## Run
```bash
python -m pip install -r requirements.txt
python run.py "Why is hybrid retrieval useful?"
```
API: `uvicorn localdoc_rag.app:app --app-dir src --host 127.0.0.1 --port 8000`
Tests: `pytest -q`
