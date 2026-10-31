# DS Week 08 — SubjectShift: Label-Efficient Wearable Recognition Under Subject Shift

**Saturday Data Science series — separate from Tuesday AI/ML engineering.**

## Problem and scientific hypothesis
Wearable activity models can memorize individual motion signatures. Test whether motion-aware masked sensor pretraining improves *unseen-person* macro-F1 in a 10% label budget, compared with frozen randomly initialized representations and competitive supervised tabular baselines. Assess calibration, subject-cluster uncertainty, sensor dropout, and selective review cost. This is a data-science investigation, not a deployed health device.

## Primary deliverable
`notebooks/DS_Week_08_SubjectShift.ipynb` — full end-to-end narrative and runnable experiments. No hosted APIs, no secrets.

## Dataset
UCI HAR (10,299 windows; 30 participants; 6 classes; CC BY 4.0). See [DATASET.md](DATASET.md). Download data with `python -c "from src.har import download; print(download())"`. No raw dataset is committed. Synthetic mode is a **smoke test only**.

## Setup and run
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux: source .venv/bin/activate
pip install -r requirements.txt
python -c "from src.har import download; print(download())"
jupyter notebook notebooks/DS_Week_08_SubjectShift.ipynb
pytest -q tests
```

Set notebook `REQUIRE_REAL=True` for research-grade run; it fails explicitly when UCI data are missing. `FAST_MODE=True` uses fewer epochs for smoke. Run from project root; notebook changes directory to project root when launched from `notebooks/`.

## Study design
- Respect UCI's official 21-subject train / 9-subject test partition; derive validation and calibration groups from training volunteers.
- Domain features: inertial-axis RMS, dispersion, jerk, spectral energy, dominant frequency, cross-axis correlations, 3D vector magnitudes. All computed from the current 2.56s window.
- Compare majority baseline, scaled multinomial logistic regression, ExtraTrees, HistGradientBoosting, random CNN frozen probe, and motion-aware masked CNN SSL frozen probe at 10% and 100% labels.
- Model selection on validation only; temperature fit on calibration only; single final test evaluation.
- Primary macro-F1, secondary balanced accuracy, log loss, ECE; subject-bootstrap 95% interval, calibration, confusion matrix, permutation importance, sensor-noise/rotation/dropout sensitivity, abstention cost.
- Contrast paper claims with independently measured results. No invented scores.

## Hardware
Ryzen 7 4800 series / 16 GB RAM / GTX 1650 Ti 4 GB: use float32, small Conv1D width=32, batch=128, 4 CPU threads, no large checkpoint, `device='cpu'` fallback. Real signals ~47 MB RAM, typical full run 2–12 minutes depending on CPU/GPU. No GPU is required.

## Interpretation
Label-efficient SSL may underperform a strong engineered-feature baseline; that is a scientifically valid result. A small test cohort and single sensor placement limit external validity. Confidence intervals clustered by subjects (not windows) mitigate correlated-window pseudo-replication. Synthetic fixture outcomes demonstrate correctness, never deployment performance.

## Resume bullet (replace outcome placeholder after real-data run)
Designed a subject-disjoint wearable sensing study comparing physics-informed inertial features and classical classifiers against motion-aware masked self-supervised representations under 10% label budgets; quantified cross-person macro-F1, cluster-bootstrap uncertainty, probability calibration, sensor-failure robustness, and selective prediction costs on the UCI HAR benchmark.

## Interview talking points
Why split by subject? Overlapping windows and individual gait make random row splits optimistic. Why pretrain only on training subjects? Avoid transductive leakage. Why macro-F1? Activity classes and safety implications are not uniform. Why cluster bootstrap? Window observations are dependent within participants. Why calibration and abstention? Risk-aware review matters beyond accuracy. Why not claim clinical utility? Dataset lacks representative patient and device variability.

## Results
`artifacts/` contains reproducible synthetic smoke outputs when real dataset is unavailable. Treat real results as pending until downloaded and rerun. See `verification.json` for executed scope.
