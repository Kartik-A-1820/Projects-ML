# DS Week 02 — Uncertainty-Aware Turbofan RUL Prognostics

Senior/Staff-adjacent predictive-maintenance study for Remaining Useful Life (RUL) estimation from multivariate turbofan trajectories.

## Scope
- manufacturing / prognostics domain
- engine-group-aware train/validation/test splitting
- leakage-safe trailing sensor features
- train-derived degradation health indicator
- Ridge + HistGradientBoosting baselines
- healthy/degraded regime-aware model
- P10/P50/P90 quantile uncertainty
- lifecycle-stage error slices
- permutation importance
- sensor-noise/drift stress tests
- asymmetric maintenance-risk cost

The notebook loads NASA C-MAPSS FD001 when `data/raw/train_FD001.txt` exists and otherwise uses a deterministic schema-compatible synthetic fleet for end-to-end smoke execution. Synthetic results are never presented as NASA benchmark results.

## Research adaptation
Inspired by Belaunzaran et al. (2026), *Bifurcated Remaining Useful Life Prediction: A Hybrid Approach for Realistic Uncertainty Characterization*. This project adapts the state-aware idea using a CPU-friendly train-derived health indicator, separate healthy/degraded gradient-boosting models, and quantile uncertainty; it does not claim to reproduce the paper's LSTM autoencoder, Weibull survival model, or probabilistic neural network.

## Hardware
Designed for Ryzen 7 4800-series CPU, 16 GB RAM and GTX 1650 Ti 4 GB. Core notebook is CPU-first and uses no paid APIs.

## Run
```bash
pip install -r requirements.txt
jupyter lab
pytest -q
```
Open `ds_week_02_turbofan_rul.ipynb`.

## Resume bullet
Built an uncertainty-aware Remaining Useful Life prognostics study for multivariate turbofan sensor trajectories using engine-group-aware validation, leakage-safe degradation health indicators, rolling/trend features, regime-aware gradient boosting and quantile prediction intervals; added lifecycle-stage error analysis, drift/noise stress tests and asymmetric maintenance-cost evaluation, with a reproducible NASA C-MAPSS notebook designed for constrained local hardware.

## Interview talking points
1. Why engine IDs must never be randomly split at row level.
2. Why trailing windows are leakage-safe but centered windows are not.
3. Why late-life optimistic RUL errors deserve separate analysis.
4. Why interval coverage must be evaluated together with width.
5. Why a train-derived health indicator can improve physical interpretability.
6. How FD002/FD004 operating-condition heterogeneity changes preprocessing.
7. How censored real fleets would shift the problem toward survival analysis.
