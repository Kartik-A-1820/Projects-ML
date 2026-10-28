# Week 11 — NLPIntent-Engine
A production-minded intent classification and out-of-domain routing engine designed for local CPU-first deployment.
## Capabilities
- TF-IDF + Logistic Regression strong baseline
- centroid-based semantic fallback using the same sparse representation
- calibrated confidence thresholding
- explicit `out_of_scope` routing
- perturbation robustness tests
- macro-F1 / accuracy / OOS precision-recall evaluation
- optional SentenceTransformer adapter point
- FastAPI interface
- deterministic sample dataset
## Hardware target
Ryzen 7 4800-series CPU, 16 GB RAM, GTX 1650 Ti 4 GB VRAM.
The default project is CPU-only and requires no model download.
Run commands from this lab's directory in an activated, isolated environment. See the [setup and contribution guide](../../CONTRIBUTING.md) before starting.
## Run
```bash
python -m pip install -r requirements.txt
python run_demo.py
python -m pytest -q
```
## API
```bash
uvicorn intent_engine.api:app --app-dir src --host 127.0.0.1 --port 8110
```
