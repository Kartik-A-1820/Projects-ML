# DS Week 04 — Censor-Aware Telecom Survival & Retention Economics
Binary churn models collapse *when* a customer will leave into yes/no and mishandle active customers whose future churn time is unknown. This lab treats retention as a right-censored time-to-event problem.
## Methodology
Kaplan–Meier reasoning, leakage-safe duration construction, discrete-time hazard ML, concordance/Brier/calibration, bootstrap uncertainty, censoring stress tests and retention economics.
## Dataset
Place IBM Telco Customer Churn-style data at `dataset/telco.csv`. Raw data is not redistributed. The notebook executes a deterministic synthetic survival fallback when absent.
Run commands from this lab's directory in an activated, isolated environment. See the [setup and contribution guide](../../CONTRIBUTING.md) before starting.
## Run
```bash
python -m pip install -r requirements.txt
jupyter nbconvert --to notebook --execute notebooks/ds_week_04_survival_retention.ipynb --output ds_week_04_survival_retention.executed.ipynb
python -m pytest -q
```
