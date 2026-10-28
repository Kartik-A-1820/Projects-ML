# DS Week 03 — Causal Uplift Modeling for Incremental Marketing Targeting
## Goal
Estimate heterogeneous treatment effects (uplift) from a randomized email experiment and convert them into a budget-aware targeting policy. The project asks a causal question—**who converts because of the intervention?**—rather than the predictive question “who is likely to convert?”
## Methodology
The notebook combines randomized-experiment reasoning, treatment-effect heterogeneity, leakage-safe feature engineering, propensity/balance diagnostics, S/T/X-style meta-learners, Qini/uplift evaluation, bootstrap uncertainty, policy value, subgroup stability, sensitivity checks, and explicit business-cost translation.
## Dataset
Primary dataset: Kevin Hillstrom's MineThatData email experiment (64,000 customers; Men's email, Women's email, or no email). The main notebook reduces it to **any email vs no email** and models conversion uplift.
Because the source dataset is not redistributed here, see `DATASET.md`. The notebook can run in:
1. **Real-data mode** when `dataset/hillstrom.csv` is present.
2. **Deterministic synthetic smoke mode** otherwise, preserving the same causal schema and randomized-treatment semantics.
Run commands from this lab's directory in an activated, isolated environment. See the [setup and contribution guide](../../CONTRIBUTING.md) before starting.
## Run
```bash
python -m pip install -r requirements.txt
jupyter nbconvert --to notebook --execute notebooks/ds_week_03_causal_uplift.ipynb --output executed.ipynb --ExecutePreprocessor.timeout=1200
python -m pytest -q
```
## Hardware
Designed for Ryzen 7 4800-series CPU, 16 GB RAM, GTX 1650 Ti 4 GB. The default models are CPU-friendly scikit-learn estimators; no GPU is required. The 64k-row Hillstrom dataset is small enough for full-data analysis.
## Design questions
- Why randomized assignment supports causal interpretation, but heterogeneous-effect estimates can still be noisy.
- Why post-treatment `visit`, `spend`, and `conversion` cannot be features.
- Why AUROC is not a valid primary metric for uplift ranking.
- Why treatment/control splitting changes variance for T-learners.
- Why targeting policy value must be estimated on held-out data.
- Why bootstrap uncertainty and subgroup stability matter before operational targeting.
- Why a response model can waste budget on “sure things” who would convert without treatment.
