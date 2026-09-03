# Week 05 — SemanticSearch-Engine (2026 Rebuild)

A local-first retrieval laboratory for **hybrid semantic + lexical search**, Reciprocal Rank Fusion (RRF), optional CrossEncoder reranking, and retrieval-quality evaluation.

## Why this project matters in 2026

Production search increasingly combines dense semantic retrieval with sparse/lexical retrieval, then optionally reranks a candidate shortlist. This avoids the common failure mode where dense retrieval misses exact identifiers while BM25 misses paraphrases.

The local default is fully dependency-light and runs without downloading a model. Dense retrieval and CrossEncoder reranking are optional adapters.

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

## Install

```bash
python -m venv .venv
pip install -r requirements.txt
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
pytest -q
```

## Resume bullet

Built an evaluable hybrid search platform combining BM25, optional dense retrieval, Reciprocal Rank Fusion and CrossEncoder reranking with metadata-aware retrieval and Recall/MRR/nDCG benchmarking; designed a production migration path covering vector/lexical stores, asynchronous indexing, multi-stage retrieval, caching, tenant isolation, observability and relevance-gated rollout.
