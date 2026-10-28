# Week 19 — DataSynth-LLM
Quality- and privacy-aware synthetic text data pipeline for creating training/evaluation corpora without treating LLM-generated data as automatically safe or useful.
## Capabilities
- template/local-generator interface
- schema/label balancing
- deduplication and near-copy screening
- PII pattern screening
- diversity scoring
- class-distribution checks
- lexical novelty / nearest-reference overlap
- synthetic-to-real utility proxy
- quality gates and reject reasons
- deterministic offline benchmark
- FastAPI generation/evaluation endpoint
## Hardware
CPU-only default. No paid API or model download required.
Run commands from this lab's directory in an activated, isolated environment. See the [setup and contribution guide](../../CONTRIBUTING.md) before starting.
## Run
```bash
python -m pip install -r requirements.txt
python run_demo.py
python evaluate.py
python -m pytest -q
```
