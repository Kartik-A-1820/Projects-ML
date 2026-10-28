# Week 23 — AutoLabel-NLP
A confidence-aware NLP labeling pipeline that combines multiple weak labelers, disagreement scoring, calibration, active-learning selection, and abstention instead of trusting one automatic annotator.
## Capabilities
- multiple rule/heuristic labelers
- probabilistic label aggregation
- disagreement/entropy scoring
- abstention policy
- active-learning review queue
- class-balance controls
- pseudo-label confidence thresholds
- held-out label-quality evaluation
- deterministic local benchmark
- optional local SLM annotator adapter point
- FastAPI endpoint
## Hardware
CPU-only default. Optional local SLM can be added later; no paid API required.
Run commands from this lab's directory in an activated, isolated environment. See the [setup and contribution guide](../../CONTRIBUTING.md) before starting.
## Run
```bash
python -m pip install -r requirements.txt
python run_demo.py
python evaluate.py
python -m pytest -q
```
