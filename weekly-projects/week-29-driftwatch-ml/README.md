# Week 29 — DriftWatch-ML

A false-alarm-aware ML monitoring engine for detecting data drift, concept drift proxies, and delayed-label performance degradation in continuously monitored production systems.

## Why this is current

Production drift monitoring suffers from a subtle operational problem: even detectors with small per-check false-positive rates can create frequent alarms when run continuously across many features. 2026 research has specifically highlighted false-alarm accumulation and detector sensitivity to batch size.

This project therefore treats **alert calibration and persistence** as first-class engineering concerns.

## Capabilities

- reference vs current feature monitoring
- KS statistic + p-value
- Population Stability Index
- lightweight linear-kernel MMD proxy
- multiple-testing correction
- minimum sample-size guard
- persistence / hysteresis alerting
- delayed-label performance monitor
- prediction-confidence distribution monitoring
- drift severity score
- detection-delay / false-alarm benchmark
- FastAPI endpoint
- deterministic synthetic stream

## Hardware

CPU-only and dependency-light. Designed for Ryzen 7 / 16 GB RAM.

## Run

```bash
pip install -r requirements.txt
python run_demo.py
python evaluate.py
pytest -q
```

## Resume bullet

Built a production ML drift-monitoring engine combining KS/PSI/MMD-style distribution tests with batch-size guards, multiple-testing correction, persistent-alert hysteresis and delayed-label performance monitoring; benchmarked false-alarm rate and detection delay under controlled shifts and designed production scaling for streaming feature windows, model/version lineage, retraining workflows, observability, multi-tenancy and incident rollback.
