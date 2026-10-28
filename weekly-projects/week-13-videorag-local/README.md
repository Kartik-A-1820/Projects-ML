# Week 13 — VideoRAG-Local
A local-first **long-video retrieval and evidence-grounding engine** designed for constrained hardware.
Instead of stuffing an entire long video into a multimodal model, the system builds event-level memory from transcript, OCR, visual captions and temporal structure, retrieves only query-relevant events, expands temporally related evidence, and returns an auditable evidence bundle.
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
Run commands from this lab's directory in an activated, isolated environment. See the [setup and contribution guide](../../CONTRIBUTING.md) before starting.
## Run
```bash
python -m pip install -r requirements.txt
python run_demo.py
python evaluate.py
python -m pytest -q
```
## API
```bash
uvicorn videorag.api:app --app-dir src --host 127.0.0.1 --port 8130
```
