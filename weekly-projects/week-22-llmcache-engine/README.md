# Week 22 — LLMCache-Engine

A calibrated, freshness-aware semantic cache for LLM/RAG serving. It separates exact hits, trusted semantic hits, near-threshold verification candidates, and misses; adds TTL/risk gates, tenant-aware cache keys, collision defenses, and deployment-oriented cache metrics.

## Why this matters in 2026
Semantic caching is now a production systems problem, not just cosine-similarity lookup. Recent work emphasizes verified promotion near thresholds, deployment calibration, freshness risk, and cache-collision robustness.

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

## Run
```bash
pip install -r requirements.txt
python run_demo.py
python evaluate.py
pytest -q
```

## Resume bullet
Built a calibrated semantic cache control plane for LLM/RAG serving with curated/dynamic tiers, freshness-aware reuse, near-threshold verification, tenant/model-version isolation and cache-quality metrics; designed production scaling for distributed cache shards, embedding services, async verification, cache poisoning defenses, telemetry, HA and rollback.
