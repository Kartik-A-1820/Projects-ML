# Week 24 — TinyLLM-FineTuner

A constrained-hardware PEFT laboratory for small language models. The project compares frozen-backbone LoRA adaptation, dynamic rank masking, and full fine-tuning on a deterministic instruction-classification benchmark while measuring accuracy, trainable parameters, wall time, and retention on a held-out general-task slice.

This modernizes the historical TinyLLM-FineTuner title into a reproducible local-specialization project rather than a one-off fine-tuning notebook.

## Why this is current
2026 PEFT research continues to optimize the quality/efficiency frontier rather than simply applying static LoRA. Recent work includes dynamic context-conditioned rank routing and systematic local-SLM benchmarking under strict hardware constraints.

## Capabilities
- tiny Transformer encoder backbone
- full fine-tuning baseline
- LoRA-injected classification head/projection
- dynamic rank masking
- deterministic benchmark dataset
- trainable-parameter and wall-time accounting
- task accuracy + retention slice
- rank/quality trade-off experiment
- CPU-first execution with CUDA support
- no paid APIs and no downloaded weights

## Hardware
Optimized for Ryzen 7 4800-series CPU, 16 GB RAM, GTX 1650 Ti 4 GB VRAM. The default model is intentionally tiny so the entire pipeline runs on CPU.

## Run
```bash
pip install -r requirements.txt
python run_benchmark.py
pytest -q
```

## Resume bullet
Built a constrained-hardware PEFT benchmarking framework for small language models comparing full fine-tuning, static LoRA, and dynamically masked low-rank adaptation; instrumented accuracy, retention, trainable-parameter ratio and wall-time trade-offs, with production architecture for quantized SLM serving, adapter registry, evaluation gates, model lineage, batching, autoscaling and rollback.
