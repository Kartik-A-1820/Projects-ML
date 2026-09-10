# Week 20 — ModelRouter-Local

A cost/quality/reliability-aware local model-routing control plane for selecting among small, medium and strong model tiers without always invoking the most expensive model.

## Why this is current in 2026
Recent routing research reframes model selection as a multi-objective decision problem across quality, cost, latency, reliability and personalization. LLMRouter (August 2026) formalizes routers using context/model encoders, scoring functions, decision rules and learning signals, while RouteLMT (April 2026) shows that routing on expected marginal gain can outperform simple difficulty heuristics.

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

## Run
```bash
pip install -r requirements.txt
python train_router.py
python run_demo.py
python evaluate.py
pytest -q
```

## Resume bullet
Built a multi-objective LLM routing control plane that learns when stronger models deliver meaningful marginal utility, enforces latency/cost/reliability constraints, performs guarded escalation and evaluates route regret, quality, cost and strong-model usage on a Pareto frontier; designed production scaling for heterogeneous local/cloud model pools, health-aware routing, telemetry, online learning, tenant budgets and safe rollback.
