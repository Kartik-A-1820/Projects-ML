# DS Week 04 — Censor-Aware Telecom Survival & Retention Economics

Binary churn models collapse *when* a customer will leave into yes/no and mishandle active customers whose future churn time is unknown. This lab treats retention as a right-censored time-to-event problem.

## Senior-level scope
Kaplan–Meier reasoning, leakage-safe duration construction, discrete-time hazard ML, concordance/Brier/calibration, bootstrap uncertainty, censoring stress tests and retention economics.

## Dataset
Place IBM Telco Customer Churn-style data at `dataset/telco.csv`. Raw data is not redistributed. The notebook executes a deterministic synthetic survival fallback when absent.

## Research adaptation
2026 work on tabular foundation models for survival regression renews interest in training-efficient censor-aware modeling. This project adapts the core question with reproducible classical/discrete-time methods suitable for Ryzen 7 / 16 GB RAM. External paper claims are not presented as project results.

## Run
```bash
pip install -r requirements.txt
jupyter nbconvert --to notebook --execute notebooks/ds_week_04_survival_retention.ipynb --output ds_week_04_survival_retention.executed.ipynb
pytest -q
```

## Resume bullet
Built a censor-aware customer-retention survival study that replaced binary churn classification with time-to-event modeling, implemented Kaplan–Meier and discrete-time hazard ML, evaluated concordance/Brier/calibration with bootstrap uncertainty and censoring stress tests, and translated survival curves into horizon-specific retention policies and customer-value decisions.
