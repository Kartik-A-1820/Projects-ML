# Week 16 — GraphRAG-Enterprise
Adaptive enterprise GraphRAG that routes simple queries to lexical retrieval, complex multi-hop queries to graph traversal, and borderline queries to fused retrieval.
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
Run commands from this lab's directory in an activated, isolated environment. See the [setup and contribution guide](../../CONTRIBUTING.md) before starting.
## Run
```bash
python -m pip install -r requirements.txt
python run_demo.py
python evaluate.py
python -m pytest -q
```
