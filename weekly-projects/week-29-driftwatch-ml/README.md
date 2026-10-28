# Week 29 — DriftWatch-ML
A false-alarm-aware ML monitoring engine for detecting data drift, concept drift proxies, and delayed-label performance degradation in continuously monitored production systems.
## Capabilities
- reference vs current feature monitoring
- KS statistic + p-value
- Population Stability Index
- lightweight linear-kernel MMD proxy
- multiple-testing correction
- minimum sample-size guard
- persistence / hysteresis alerting
- delayed-label performance monitor
- prediction-confidence distribution monitoring
- drift severity score
- detection-delay / false-alarm benchmark
- FastAPI endpoint
- deterministic synthetic stream
## Hardware
CPU-only and dependency-light. Designed for Ryzen 7 / 16 GB RAM.
Run commands from this lab's directory in an activated, isolated environment. See the [setup and contribution guide](../../CONTRIBUTING.md) before starting.
## Run
```bash
python -m pip install -r requirements.txt
python run_demo.py
python evaluate.py
python -m pytest -q
```
