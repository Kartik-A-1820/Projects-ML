# DS Week 01 — Calibrated Credit Risk Under Shift

**Portfolio track:** Senior Data Scientist / Applied Scientist  
**Domain:** Fintech / credit risk  
**Primary artifact:** `ds_week_01_credit_risk.ipynb`

This project treats credit default prediction as a probability-estimation and decision-quality problem rather than a binary-classification demo. It benchmarks transparent and nonlinear tabular models, engineers leakage-safe behavioral features, calibrates probabilities, optimizes thresholds under asymmetric costs, adds split-conformal uncertainty, diagnoses subgroup slices, and stress-tests controlled covariate shift.

## Dataset
UCI **Default of Credit Card Clients** — 30,000 rows, 23 explanatory features, binary next-month default target. Raw data is not committed; see `DATASET.md`.

## Senior Data Scientist signals
- explicit leakage audit and held-out calibration split
- domain features for utilization, repayment and delinquency dynamics
- Logistic Regression vs HistGradientBoosting comparison
- ROC-AUC, PR-AUC, Brier, log loss, ECE and Recall@5% FPR
- Platt calibration and business-cost thresholding
- split conformal prediction sets
- permutation importance on held-out data
- sensitive/proxy attributes excluded from model and used only for diagnostics
- controlled distribution-shift stress tests
- clear limits: stress tests are not a temporal validation claim

## Local hardware
Designed for Ryzen 7 4800-series CPU, 16 GB RAM and GTX 1650 Ti 4 GB VRAM. Default workflow is CPU-first.

## Run
```bash
python -m venv .venv
pip install -r requirements.txt
jupyter lab ds_week_01_credit_risk.ipynb
```

The checked-in notebook defaults to `SMOKE_MODE=True` so it can execute without network access using a deterministic schema-compatible dataset. Set it to `False` for the full UCI dataset.

## Verify
```bash
pytest -q
python scripts_smoke.py
```

## Resume bullet
Designed a calibrated credit-risk modeling framework for tabular financial data, engineering leakage-safe utilization/delinquency/payment dynamics, benchmarking linear and gradient-boosted models, optimizing thresholds under asymmetric decision costs, adding split-conformal uncertainty, and stress-testing discrimination/calibration across covariate shifts and demographic slices; packaged the analysis as a reproducible, hardware-efficient research notebook with production monitoring recommendations.
