# Week 16 — GraphRAG-Enterprise

Adaptive enterprise GraphRAG that routes simple queries to lexical retrieval, complex multi-hop queries to graph traversal, and borderline queries to fused retrieval.

## Why this matters
Recent GraphRAG work shows that always invoking graph retrieval can increase latency and even reduce quality on simple questions. This project treats graph retrieval as an adaptive capability, not a default hammer.

## Capabilities
- deterministic enterprise knowledge graph construction from structured triples
- BM25 lexical retrieval
- entity-aware graph traversal
- query complexity scoring
- adaptive routing: lexical / graph / hybrid
- Reciprocal Rank Fusion
- provenance-preserving evidence paths
- Recall@K, MRR and path-coverage evaluation
- FastAPI endpoint
- production design for hybrid graph/vector/search infrastructure

## Hardware
CPU-first. No model downloads required. Suitable for Ryzen 7 / 16 GB RAM / GTX 1650 Ti 4 GB.

## Run
```bash
pip install -r requirements.txt
python run_demo.py
python evaluate.py
pytest -q
```

## Resume bullet
Built an adaptive enterprise GraphRAG engine that dynamically routes queries between lexical and graph retrieval based on measured complexity, preserves multi-hop evidence paths and fuses borderline cases with RRF; designed production scaling across graph/vector/search stores, async ingestion, model/index lineage, tenant isolation, graph partitioning, observability, rollback and cost-aware routing.
