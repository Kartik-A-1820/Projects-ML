# Week 23 — AutoLabel-NLP

A confidence-aware NLP labeling pipeline that combines multiple weak labelers, disagreement scoring, calibration, active-learning selection, and abstention instead of trusting one automatic annotator.

## Why this matters in 2026
Modern annotation systems increasingly use LLMs/SLMs as annotators, but recent AAAI 2026 work shows single-model labels remain noisy. Stronger systems combine multiple annotators, explicitly model disagreement, and focus human review on uncertain/high-value examples.

## Capabilities
- multiple rule/heuristic labelers
- probabilistic label aggregation
- disagreement/entropy scoring
- abstention policy
- active-learning review queue
- class-balance controls
- pseudo-label confidence thresholds
- held-out label-quality evaluation
- deterministic local benchmark
- optional local SLM annotator adapter point
- FastAPI endpoint

## Hardware
CPU-only default. Optional local SLM can be added later; no paid API required.

## Run
```bash
pip install -r requirements.txt
python run_demo.py
python evaluate.py
pytest -q
```

## Resume bullet
Built an active weak-supervision labeling system that aggregates multiple noisy NLP labelers, quantifies disagreement/entropy, abstains on low-confidence examples and prioritizes review with active-learning scores; added label-quality evaluation, class-balance monitoring and a production design for local SLM annotators, human review queues, dataset lineage, observability and safe pseudo-label promotion.
