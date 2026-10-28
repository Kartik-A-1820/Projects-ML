# DS Week 02 — Uncertainty-Aware Turbofan RUL Prognostics
Predictive-maintenance study for Remaining Useful Life (RUL) estimation from multivariate turbofan trajectories.
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
## Hardware
Designed for Ryzen 7 4800-series CPU, 16 GB RAM and GTX 1650 Ti 4 GB. Core notebook is CPU-first and uses no paid APIs.
Run commands from this lab's directory in an activated, isolated environment. See the [setup and contribution guide](../../CONTRIBUTING.md) before starting.
## Run
```bash
python -m pip install -r requirements.txt
jupyter lab
python -m pytest -q
```
Open `ds_week_02_turbofan_rul.ipynb`.
## Design questions
1. Why engine IDs must never be randomly split at row level.
2. Why trailing windows are leakage-safe but centered windows are not.
3. Why late-life optimistic RUL errors deserve separate analysis.
4. Why interval coverage must be evaluated together with width.
5. Why a train-derived health indicator can improve physical interpretability.
6. How FD002/FD004 operating-condition heterogeneity changes preprocessing.
7. How censored real fleets would shift the problem toward survival analysis.
