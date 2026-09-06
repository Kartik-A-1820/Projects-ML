# Week 12 — ModelExplain-ML (2026 Rebuild)

A local explainable-ML laboratory for tabular risk models. It combines predictive performance, calibration, global permutation importance, partial dependence, local surrogate attribution and actionability-aware counterfactual search.

## Why this project is current

Explainability in 2026 is increasingly evaluated as an engineering property: fidelity to the underlying model, stability across nearby samples, latency, actionability, separation of mutable vs immutable features, and reproducibility under model/data versions.

Recent work such as ShapPFN explores generating high-fidelity explanations dramatically faster than KernelSHAP for tabular models. This project stays dependency-light but adopts the same production principle: explanation quality and latency must be measured.

## Capabilities

- synthetic credit-risk style tabular dataset
- HistGradientBoosting risk model
- probability calibration metrics
- held-out permutation importance
- partial dependence
- local perturbation surrogate explanations
- immutable/mutable feature policy
- constrained counterfactual search
- explanation stability metric
- tests + smoke workflow

## Hardware
CPU-first and comfortably within Ryzen 7 / 16 GB RAM.

## Run
```bash
pip install -r requirements.txt
python run_demo.py
pytest -q
```

## Resume bullet
Built an explainable tabular ML framework that pairs calibrated gradient boosting with held-out permutation importance, partial dependence, local surrogate explanations, stability testing and actionability-constrained counterfactual search; designed production controls for explanation fidelity, model/version lineage, immutable-feature policies, auditability and regulated decision-support workflows.
