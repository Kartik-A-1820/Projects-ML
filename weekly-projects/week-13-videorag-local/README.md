# Week 13 — VideoRAG-Local (2026 Rebuild)

A local-first **long-video retrieval and evidence-grounding engine** designed for constrained hardware.

Instead of stuffing an entire long video into a multimodal model, the system builds event-level memory from transcript, OCR, visual captions and temporal structure, retrieves only query-relevant events, expands temporally related evidence, and returns an auditable evidence bundle.

## 2026 design direction

Long-video RAG research has moved beyond flat independent clip retrieval. VideoStir (ACL 2026) uses spatio-temporal structure and intent-aware retrieval; CARVE/V-RAGBench (June 2026) evaluates retrieval separately and adapts modality/granularity per chunk; Event-Causal RAG represents long video as coherent events and causal structure.

This project adapts those principles into a lightweight implementation that runs without downloading a large VLM.

## Capabilities

- event-level timeline representation
- transcript / OCR / visual-caption modalities
- modality-specific BM25 retrieval
- query-intent-aware modality weighting
- Reciprocal Rank Fusion
- temporal-neighbor expansion
- simple event-link graph
- evidence budgets and deduplication
- explicit timestamps/citations
- retrieval Recall@K, MRR and temporal coverage
- optional Whisper / Qwen2.5-VL adapter points
- FastAPI search endpoint
- deterministic synthetic evaluation

## Hardware target

Ryzen 7 4800-series CPU, 16 GB RAM, GTX 1650 Ti 4 GB VRAM.

Recommended local strategy:
- CPU extraction/retrieval;
- Whisper `tiny`/`base` or faster-whisper only when transcription is needed;
- sampled keyframes rather than every frame;
- small VLM only for selected frames if used at all;
- persist derived event memory so video analysis is not repeated per query.

## Run

```bash
python -m venv .venv
pip install -r requirements.txt
python run_demo.py
python evaluate.py
pytest -q
```

## API

```bash
uvicorn videorag.api:app --app-dir src --host 127.0.0.1 --port 8130
```

## Resume bullet

Built a structured long-video RAG engine that indexes transcript, OCR and visual evidence as event memory, performs intent-aware multi-modal retrieval with RRF and temporal-neighbor expansion, and evaluates retrieval independently with Recall/MRR/temporal coverage; architected scalable asynchronous video ingestion, CPU/GPU model routing, event-graph storage, evidence budgets, traceability and multimodal quality monitoring.
