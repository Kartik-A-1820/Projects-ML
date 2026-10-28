# Week 22 — LLMCache-Engine
A calibrated, freshness-aware semantic cache for LLM/RAG serving. It separates exact hits, trusted semantic hits, near-threshold verification candidates, and misses; adds TTL/risk gates, tenant-aware cache keys, collision defenses, and deployment-oriented cache metrics.
## Capabilities
- exact + semantic response cache
- deterministic local embedding proxy
- threshold calibration from labeled pairs
- static curated + dynamic cache tiers
- freshness/TTL risk gate
- near-threshold async verification queue
- tenant/model/prompt-version isolation
- cache-collision defense hooks
- precision, hit ratio, stale-error and avoided-inference accounting
- FastAPI endpoint
## Hardware
CPU-only default; no model downloads. Optional production adapter can use a small sentence-transformer on CPU/GPU.
Run commands from this lab's directory in an activated, isolated environment. See the [setup and contribution guide](../../CONTRIBUTING.md) before starting.
## Run
```bash
python -m pip install -r requirements.txt
python run_demo.py
python evaluate.py
python -m pytest -q
```
