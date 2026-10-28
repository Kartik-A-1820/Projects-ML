# DS Week 07 — Phishing Detection Under Unseen-Domain Shift
**Primary notebook:** `notebooks/DS_Week_07_Phishing_Domain_Generalization.ipynb`.
## Decision problem
Can a URL-only phishing detector generalize to **unseen registrable domains**, maintain calibrated probabilities and minimize analyst false positives while controlling missed attacks? Random URL splits can overstate performance due to domain overlap. Evaluate domain-disjoint partitions and never fit preprocessing on holdout data.
## Dataset
UCI PhiUSIIL URL (CC BY 4.0), 235,795 observations; see `DATASET.md`. Download and extract CSV into `data/PhiUSIIL_Phishing_URL_Dataset.csv`. Raw data is not committed. When absent the notebook runs a labeled **synthetic smoke test** only.
Run commands from this lab's directory in an activated, isolated environment. See the [setup and contribution guide](../../CONTRIBUTING.md) before starting.
## Reproduce
```bash
python -m pip install -r requirements.txt
# Optional: pip install torch
jupyter lab notebooks/DS_Week_07_Phishing_Domain_Generalization.ipynb
PYTHONPATH=src python -m pytest -q tests
```
Notebook cells run sequentially; add `src/` to sys.path automatically. Optional torch model is skipped with an explicit status if PyTorch unavailable. All other methods run on CPU. A scriptable notebook run is possible with `jupyter nbconvert --to notebook --execute ...`.
## Experimental design
1. Explicit target (`1=phishing`), deduplicate conflicting URLs and repeated URLs, missingness/outlier/imbalance audit.
2. Derive URL-only lexical/security features; no website scraping, label statistics, domain IDs or target encoding.
3. Train/validation/calibration/test split by domain group; train-only scaler and imputation.
4. Baselines: logistic regression, histogram gradient boosting, ExtraTrees; optional lightweight parameter-shared neural ensemble.
5. Select model using validation PR-AUC; fit sigmoid calibration on a separate calibration partition; evaluate once on untouched domain-held-out test.
6. Report PR-AUC, ROC-AUC, Brier, log loss, F1, false positives, false negatives, cost-per-URL, grouped bootstrap CIs, feature permutation importance, error slices, tracking-query perturbation robustness, calibration and cost sensitivity.
7. Distinguish synthetic smoke results from real UCI results. Do not claim deployment readiness without temporal, external-dataset and adversarial evaluations.
## Hardware
Ryzen 7 4800-series, 16 GB RAM, GTX 1650 Ti 4 GB VRAM. Classical models use CPU with <=4 workers; 20 float32 features (~20 MB for 235k rows), moderate ExtraTrees memory (typically <2 GB). CPU baseline typically minutes, depends on laptop. Optional torch ensemble k=4, hidden sizes 48/24, batch 512, <=18 epochs with early stopping, CPU fallback. Avoid heavy pretrained models. Benchmark run times are environment-dependent, not promises.
## Design questions
- Why group by domain rather than random URLs? Prevent memorizing host-level artifacts; related domains remain a limitation.
- Why not include webpage-content and UCI aggregate probability fields? Availability and provenance at decision time are uncertain.
- Why four splits? Separate model selection, probability calibration and untouched final test.
- Why PR-AUC and business costs? Phishing prevalence and asymmetric error costs.
- Why not claim a temporal benchmark? UCI lacks reliable per-row observation timestamps.
- Why not claim TabM reproduction? This is a constrained parameter-sharing adaptation; the official paper uses a richer design.
## Limitations and follow-ups
Real-time prevalence drift, root-domain grouping approximations, URL label noise, browser redirect effects, attacks via benign compromised domains, external validation, adversarial perturbations, and governance around automated blocking. Follow up with time-stamped feed data, PSL-pinned domains, selective abstention, calibrated alert budgets, and external cross-dataset testing.
## Verified run — 24 Oct 2026
Executed end-to-end on **2,000 synthetic URLs from 500 reserved `.example` domains** because the real UCI archive was not reachable from this workspace. This is a reproducibility and logic test, **not a valid real phishing benchmark**. Logistic regression was the selected classical model. Synthetic held-out PR-AUC=0.7255, ROC-AUC=0.7582, Brier=0.1958, 95% domain-bootstrap PR-AUC CI=[0.6203,0.8224]. The cost-based threshold (1/6) yielded 165 false positives and 2 false negatives on 300 synthetic held-out URLs. The benign tracking-query perturbation flipped 46% of thresholded decisions, exposing a significant robustness limitation rather than hiding it. The optional small neural ensemble completed on CPU. All five tests passed. See `artifacts/synthetic_smoke_metrics.json` and `verification.json`.
