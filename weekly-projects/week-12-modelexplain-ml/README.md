# Week 12 — ModelExplain-ML
A local explainable-ML laboratory for tabular risk models. It combines predictive performance, calibration, global permutation importance, partial dependence, local surrogate attribution and actionability-aware counterfactual search.
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
Run commands from this lab's directory in an activated, isolated environment. See the [setup and contribution guide](../../CONTRIBUTING.md) before starting.
## Run
```bash
python -m pip install -r requirements.txt
python run_demo.py
python -m pytest -q
```
