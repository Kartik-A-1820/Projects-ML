# DS Week 06 — Drift-Aware Multi-Station PM2.5 Forecasting with Delayed-Feedback Conformal Intervals

**Series:** Saturday Data Science Labs, independent of Tuesday AI/ML engineering. **Level:** Senior/Staff-adjacent Data Scientist. **Domain:** environment / public health / climate.

## Business question
Predict PM2.5 at 12 Beijing monitoring stations **24 hours ahead**, with honest uncertainty bounds despite seasonal changes, extreme events, missing sensors, spatial transfer, and a full 24-hour delay before forecast errors can be observed. Decision-makers need not just a low MAE but timely, calibrated risk ranges for pollution alerts.

## Dataset and research
Primary: UCI Beijing Multi-Site Air Quality, 420,768 hourly records, 12 sites, March 2013–February 2017, CC BY 4.0. See DATASET.md. Raw data not committed. Automatic synthetic fallback is for executable smoke tests **only**.

Research adaptation: Bias-Corrected Adaptive Conformal Inference (BC-ACI, 2026 preprint) and Adaptive Conformal Inference (Gibbs & Candès). We **do not reproduce their published results**. We implement split-conformal, conformalized quantile regression, and a delay-aware online rolling/alpha-adaptive conformal variant, then compare empirical coverage, width, interval score and station/extreme-pollution slices.

## Run
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate ; Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
pytest -q
jupyter nbconvert --to notebook --execute notebooks/ds_week_06_airquality_conformal.ipynb --output executed.ipynb --ExecutePreprocessor.timeout=1800
```
To use real data, download the official UCI archive, extract its twelve `PRSA_Data_*.csv` files into `dataset/raw/`, then rerun. The notebook auto-detects them. See DATASET.md. Results must identify whether they used UCI or SYNTHETIC.

## Research design and trustworthiness
- Forecast origin t: predict PM2.5 at t+24h using only sensor/weather measurements available at or before t. **No future observed weather.**
- Reindex each station to a regular hourly grid before lagging/shift; missing targets excluded, feature missingness retained.
- Strict global chronological train → validation (model selection) → calibration (interval construction) → test. A training example is eligible only if **its target timestamp** falls within its split; never train on labels arriving after the split boundary.
- Hold out two entire stations from fitting and calibration; they remain in evaluation as a telemetry-available spatial-transfer stress test. No exchangeability/coverage guarantee is claimed for these sites.
- Model candidates: seasonal naive 24h persistence, regularized Ridge, histogram gradient boosting. Quantile gradient boosting forms base CQR intervals.
- Intervals: split conformal, CQR, delayed-feedback adaptive CQR. Updates use only errors whose 24h targets have matured.
- Compare MAE/RMSE, 90% coverage, interval width, Winkler interval score, site and high-pollution slices, and monthly stability. Station-block bootstrap is recommended for full inference; simple row bootstrap understates serial dependence.

## Hardware
CPU-first, float32, ~0.5M rows, ~35 numeric/categorical features. Typical 16 GB RAM adequate; no GPU required. HistGradientBoosting and small Ridge are robust CPU baselines. `FAST_MODE=1` uses fewer boosting iterations for development, without sampling evaluation rows. Synthetic fallback ~6 stations / 2 years, fast enough for smoke tests. A TCN/TFT extension must be explicitly benchmarked against these strong tabular baselines before being called better.

## Resume bullet
Designed and evaluated a leakage-audited, multi-station 24-hour PM2.5 forecasting study using station-aware temporal features, chronological/spatial holdouts, Ridge and boosted-tree baselines, CQR and delayed-feedback adaptive conformal intervals, interval-score optimization, extreme-event slices, sensitivity analysis and reproducible experiment artifacts.

## Interview discussion
Why target timestamps—not only feature timestamps—determine split boundaries; why same-day weather forecasts cannot be replaced with future observed weather; why marginal coverage does not imply per-station coverage; why a 24h feedback delay matters for adaptive conformal methods; when adaptive uncertainty improves alerting despite point forecast accuracy remaining unchanged.

## Files
`notebooks/` main executable narrative; `src/` reusable leakage-safe feature/interval methods; `tests/` unit checks; `artifacts/` JSON and plots from last executed run; `configs/` deterministic settings; `DS_PROJECT_REGISTRY.json` continuity.