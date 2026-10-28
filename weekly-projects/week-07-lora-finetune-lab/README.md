# Week 07 — LoRA-FineTune-Lab
A resource-aware PEFT laboratory for instruction fine-tuning small language models on consumer hardware. It supports dry-run dataset validation on CPU and an optional QLoRA training path with Hugging Face Transformers + PEFT + TRL.
## What this demonstrates
- instruction dataset schema/quality validation
- train/validation split discipline
- QLoRA configuration for constrained VRAM
- LoRA rank/alpha/dropout trade-offs
- adapter-only checkpoints
- exact-match / structure-aware evaluation harness
- catastrophic-forgetting guardrail examples
- reproducible experiment manifests
## Hardware target
Ryzen 7 4800-series, 16 GB RAM, GTX 1650 Ti 4 GB VRAM.
The default example targets `Qwen/Qwen2.5-0.5B-Instruct` because 4 GB VRAM is the hard constraint. Training uses 4-bit NF4 where bitsandbytes/CUDA support is available; otherwise the project can validate data/config/evaluation without training.
Run commands from this lab's directory in an activated, isolated environment. See the [setup and contribution guide](../../CONTRIBUTING.md) before starting.
## Quick start
```bash
python -m pip install -r requirements.txt
python validate_dataset.py
python run_smoke.py
```
## Optional QLoRA training
```bash
python train_qlora.py --max-steps 30
```
## Evaluate adapter outputs
```bash
python evaluate.py --predictions data/sample_predictions.json
```
