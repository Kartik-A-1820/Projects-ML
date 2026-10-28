# Week 31 — ContinualLearn-NLP
A resource-efficient continual-learning laboratory for NLP systems that must learn sequential domains without catastrophically forgetting earlier capabilities.
## Industry problem
Production language systems change continuously: support intents evolve, product taxonomies expand, fraud/security language shifts, and enterprise policies change. Re-training from scratch is expensive; naive sequential fine-tuning can erase prior capabilities.
## Local implementation
- deterministic hashing text representation;
- expandable softmax classifier;
- stability regularization against the previous parameter anchor;
- bounded replay memory;
- forgetting-priority replay;
- sequential task stream;
- per-task accuracy, average accuracy and forgetting metrics;
- replay vs no-replay benchmark.
This dependency-light core runs on CPU and verifies the continual-learning control plane without model downloads. For the full experiment, replace the encoder/classifier with a 0.5B–1.5B local SLM plus LoRA/QLoRA while keeping replay/evaluation unchanged.
Run commands from this lab's directory in an activated, isolated environment. See the [setup and contribution guide](../../CONTRIBUTING.md) before starting.
## Run
```bash
python -m pip install -r requirements.txt
python run_demo.py
python evaluate.py
python -m pytest -q
```
## Hardware strategy
Ryzen 7/16 GB: CPU core is trivial. GTX 1650 Ti 4 GB: use <=1.5B model, 4-bit base weights, LoRA rank 4–8, sequence length 256–512, batch 1–2 with gradient accumulation. Do not train a multi-billion-parameter model from scratch.
## Experiments
1. sequential training without replay;
2. fixed replay;
3. forgetting-priority replay;
4. replay-capacity sweep;
5. regularization sweep;
6. optional LoRA backend;
7. task-order sensitivity.
Measure final average accuracy, backward transfer/forgetting, memory footprint, task adaptation accuracy and wall-clock cost.
