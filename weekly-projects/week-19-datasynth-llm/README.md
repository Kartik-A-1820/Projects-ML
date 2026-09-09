# Week 19 — DataSynth-LLM

Quality- and privacy-aware synthetic text data pipeline for creating training/evaluation corpora without treating LLM-generated data as automatically safe or useful.

## Why this matters now
2026 synthetic-data research emphasizes a three-way trade-off: utility, diversity/fidelity, and privacy. Synthetic data can amplify bias, memorize training examples, or contaminate future model training if quality checks are skipped.

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

## Run
```bash
pip install -r requirements.txt
python run_demo.py
python evaluate.py
pytest -q
```

## Resume bullet
Built a governance-first synthetic text data pipeline that generates balanced task data, rejects PII and near-copies, scores diversity/novelty and evaluates downstream utility before promotion; designed production scaling for private seed handling, DP-aware candidate selection, generator/model lineage, distributed quality gates, dataset registry, auditability and contamination-safe rollout.
