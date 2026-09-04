# Week 08 — MultiPDF-RAG (2026 Rebuild)

A citation-first multi-document RAG system with document/page provenance, hybrid lexical+dense retrieval, Reciprocal Rank Fusion, optional reranking, evidence sufficiency checks and retrieval evaluation.

## Features
- PDF/text ingestion abstraction
- page-aware chunking
- BM25 lexical retrieval
- optional SentenceTransformer dense retrieval
- RRF fusion
- optional CrossEncoder reranking
- citation-preserving context
- extractive evidence answer fallback
- Recall@K/MRR evaluation fixture
- FastAPI query endpoint

## Hardware target
Ryzen 7 4800-series, 16 GB RAM, GTX 1650 Ti 4 GB VRAM.

Default smoke path is CPU-only. Dense retrieval/reranking are optional. A local generator can be added later, but the core project deliberately evaluates retrieval before adding generation.

## Run
```bash
pip install -r requirements.txt
python run_demo.py "What does policy AC-17 require?"
pytest -q
```

## Optional PDF support
```bash
pip install pymupdf
```

## Resume bullet
Built a citation-first multi-document RAG platform with page-aware ingestion, hybrid BM25/dense retrieval, RRF fusion, optional CrossEncoder reranking, evidence sufficiency gates and Recall/MRR evaluation; designed a production architecture for asynchronous PDF ingestion, index versioning, ACL-aware retrieval, scalable model serving, claim grounding and tenant isolation.
