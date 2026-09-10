# Week 21 — HybridSearch-RAG

An adaptive retrieval laboratory for RAG that goes beyond the earlier Week 05/08 hybrid-search work by learning which retrieval/fusion policy to use for each query family.

This project benchmarks exact-ID, semantic/paraphrase and mixed queries; routes them to sparse, semantic-proxy or hybrid retrieval; compares RRF against normalized weighted fusion; applies lightweight pseudo-relevance feedback; and evaluates quality and candidate-budget trade-offs.

## Why this is current in 2026
Recent hybrid-retrieval research continues to find complementary failure modes between sparse and dense retrieval. The engineering question is no longer merely “use BM25 + vectors”, but how to allocate retrieval and reranking work per query while measuring quality/latency trade-offs.

## Distinct from earlier weeks
- Week 05: foundational sparse+dense retrieval and RRF
- Week 08: citation-first MultiPDF RAG
- Week 21: adaptive query-family routing, fusion-strategy comparison, PRF and per-route budgets

## Capabilities
- BM25 sparse retrieval
- lightweight latent-semantic dense proxy using TF-IDF + TruncatedSVD
- query-family classifier: exact / semantic / mixed
- sparse-only, dense-only and hybrid paths
- RRF and normalized weighted fusion
- pseudo-relevance-feedback expansion
- per-query candidate budgets
- Recall@K, MRR, nDCG@K and route-specific evaluation
- FastAPI endpoint

## Hardware
CPU-only by default; no model download. Production can replace the semantic proxy with BGE/E5/SPLADE and add a cross-encoder reranker.

## Run
```bash
pip install -r requirements.txt
python run_demo.py
python evaluate.py
pytest -q
```

## Resume bullet
Built an adaptive hybrid-retrieval engine for production RAG that classifies query families, dynamically selects sparse/dense/hybrid paths, compares RRF with normalized score fusion, applies pseudo-relevance feedback and enforces candidate budgets; evaluated route-specific Recall/MRR/nDCG and designed production scaling for dual indexes, reranking, query routing, index lineage, caching, multi-tenancy and relevance-gated rollout.
