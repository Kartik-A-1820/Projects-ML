# Week 20 — ModelRouter-Local
A cost/quality/reliability-aware local model-routing control plane for selecting among small, medium and strong model tiers without always invoking the most expensive model.
## Capabilities
- explicit model capability/cost/latency registry
- learned lightweight marginal-gain router
- budget/latency/reliability constraints
- guarded escalation and circuit-breaker inputs
- cost-quality Pareto evaluation
- route regret and strong-model-call-rate metrics
- deterministic tests and FastAPI endpoint
## Hardware target
Ryzen 7 4800-series CPU, 16 GB RAM, GTX 1650 Ti 4 GB VRAM. The router itself is CPU-only; real target models may be local quantized SLMs.
Run commands from this lab's directory in an activated, isolated environment. See the [setup and contribution guide](../../CONTRIBUTING.md) before starting.
## Run
```bash
python -m pip install -r requirements.txt
python train_router.py
python run_demo.py
python evaluate.py
python -m pytest -q
```
