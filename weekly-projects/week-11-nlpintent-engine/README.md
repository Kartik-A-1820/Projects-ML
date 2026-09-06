# Week 11 — NLPIntent-Engine (2026 Rebuild)

A production-minded intent classification and out-of-domain routing engine designed for local CPU-first deployment.

## Why this project is current

Intent classification is no longer only a closed-set accuracy problem. Modern systems must handle:
- few-shot / low-data intent classes,
- confidence calibration,
- out-of-scope (OOS) detection,
- perturbation robustness,
- efficient open-weight deployment,
- explainable fallback behavior.

A July 2026 systematic study of 41 open-weight models found that deployment efficiency, calibration and robustness materially affect model selection, and that older benchmarks such as SNIPS are becoming saturated.

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

## Run

```bash
pip install -r requirements.txt
python run_demo.py
pytest -q
```

## API

```bash
uvicorn intent_engine.api:app --app-dir src --host 127.0.0.1 --port 8110
```

## Resume bullet

Built a calibrated intent-routing engine with strong sparse baselines, confidence-aware out-of-scope rejection, perturbation robustness testing and explicit fallback behavior; designed production scaling for multilingual embedding classifiers, active-learning feedback, per-intent calibration, drift monitoring, tenant-specific label spaces and low-latency CPU/GPU serving.
