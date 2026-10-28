# Week 18 — RAGGuard-Local
Layered security middleware for retrieval-augmented generation systems. It defends the knowledge-access pipeline against direct prompt injection, indirect prompt injection in retrieved documents, knowledge poisoning, context exfiltration attempts, and unsafe downstream output.
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
Run commands from this lab's directory in an activated, isolated environment. See the [setup and contribution guide](../../CONTRIBUTING.md) before starting.
## Run
```bash
python -m pip install -r requirements.txt
python run_demo.py
python evaluate.py
python -m pytest -q
```
