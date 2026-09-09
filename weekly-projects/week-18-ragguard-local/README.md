# Week 18 — RAGGuard-Local

Layered security middleware for retrieval-augmented generation systems. It defends the knowledge-access pipeline against direct prompt injection, indirect prompt injection in retrieved documents, knowledge poisoning, context exfiltration attempts, and unsafe downstream output.

## Why this matters now
2026 RAG security work increasingly treats security as a pipeline problem rather than a single input-filter problem. Recent frameworks emphasize layered controls across user input, retrieved context, provenance, and output auditing.

## Capabilities
- Unicode normalization and invisible-character stripping
- direct prompt-injection detection
- retrieved-document trust scoring
- indirect-injection scanning
- provenance-aware context assembly
- instruction/data boundary enforcement
- output leakage auditing
- structured security trace
- attack-success / false-positive evaluation
- FastAPI middleware endpoint
- deterministic offline tests

## Hardware
CPU-only by default. No model download required. Runs comfortably on Ryzen 7 / 16 GB RAM.

## Run
```bash
pip install -r requirements.txt
python run_demo.py
python evaluate.py
pytest -q
```

## Resume bullet
Built a layered RAG security control plane that normalizes hostile Unicode, detects direct and indirect prompt injection, scores retrieved-document trust, enforces provenance-aware instruction boundaries and audits outputs for leakage; added attack/benign evaluation, structured traces and a production design spanning secure ingestion, retrieval ACLs, model/tool policy, telemetry, multi-tenancy and rollback.
