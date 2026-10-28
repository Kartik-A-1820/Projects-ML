# Week 08 — MultiPDF-RAG
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
Run commands from this lab's directory in an activated, isolated environment. See the [setup and contribution guide](../../CONTRIBUTING.md) before starting.
## Run
```bash
python -m pip install -r requirements.txt
python run_demo.py "What does policy AC-17 require?"
python -m pytest -q
```
## Optional PDF support
```bash
python -m pip install pymupdf
```
