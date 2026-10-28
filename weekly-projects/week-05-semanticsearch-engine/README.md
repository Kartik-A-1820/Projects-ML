# Week 05 — SemanticSearch-Engine
A local-first retrieval laboratory for **hybrid semantic + lexical search**, Reciprocal Rank Fusion (RRF), optional CrossEncoder reranking, and retrieval-quality evaluation.
## Features
- BM25 lexical retrieval implemented locally
- optional SentenceTransformer dense retrieval
- Reciprocal Rank Fusion
- optional CrossEncoder reranker
- deterministic document IDs
- metadata filtering
- Recall@K, MRR and nDCG@K evaluation
- FastAPI service
- synthetic benchmark corpus
- production architecture for Qdrant/OpenSearch/pgvector style deployments
## Local hardware target
Ryzen 7 4800-series CPU, 16 GB RAM, GTX 1650 Ti 4 GB VRAM.
For local development:
- BM25 on CPU
- MiniLM-family dense embeddings on CPU by default
- optional small CrossEncoder on CPU/GPU
- no always-on vector database required
Run commands from this lab's directory in an activated, isolated environment. See the [setup and contribution guide](../../CONTRIBUTING.md) before starting.
## Install
```bash
python -m pip install -r requirements.txt
```
## Smoke demo
```bash
python run_demo.py "error code E104 payment timeout"
```
## Evaluate lexical/hybrid-compatible pipeline
```bash
python evaluate.py
```
## API
```bash
uvicorn semantic_search.api:app --app-dir src --host 127.0.0.1 --port 8050
```
## Tests
```bash
python -m pytest -q
```
