# DATASET.md
Primary dataset: IBM Telco Customer Churn-style snapshot data. Expected local path: `dataset/telco.csv`.

Survival construction: duration = observed tenure; event = 1 for churned and 0 for active/right-censored customers. This is a pragmatic retrospective formulation; production should reconstruct start/event/censor dates from longitudinal subscription tables.

Leakage: exclude customer ID and all post-snapshot cancellation, support and payment information.

Raw data is not committed because mirrors can carry different terms. Review source terms at download time. A deterministic synthetic fallback verifies execution offline.
