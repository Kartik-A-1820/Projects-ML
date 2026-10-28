# Week 24 — TinyLLM-FineTuner
A constrained-hardware PEFT laboratory for small language models. The project compares frozen-backbone LoRA adaptation, dynamic rank masking, and full fine-tuning on a deterministic instruction-classification benchmark while measuring accuracy, trainable parameters, wall time, and retention on a held-out general-task slice.
This modernizes the historical TinyLLM-FineTuner title into a reproducible local-specialization project rather than a one-off fine-tuning notebook.
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
Run commands from this lab's directory in an activated, isolated environment. See the [setup and contribution guide](../../CONTRIBUTING.md) before starting.
## Run
```bash
python -m pip install -r requirements.txt
python run_benchmark.py
python -m pytest -q
```
