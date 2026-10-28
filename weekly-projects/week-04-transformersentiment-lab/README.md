# Week 04 — TransformerSentiment-Lab
A rigorous transformer classification lab for TweetEval sentiment. The project emphasizes leakage-safe benchmark protocol, a strong sparse baseline, efficient encoder fine-tuning, calibration, and slice/error analysis.
## Model strategy
Default deep model: `microsoft/deberta-v3-small`.
For stable labeled classification, a compact encoder is faster and cheaper than a generative LLM classifier. The training recipe targets GTX 1650 Ti 4 GB using max length 128, batch size 4, gradient accumulation, gradient checkpointing, and FP16 when available.
## Dataset
TweetEval `sentiment` is downloaded at runtime through Hugging Face Datasets. No dataset rows are committed.
Run commands from this lab's directory in an activated, isolated environment. See the [setup and contribution guide](../../CONTRIBUTING.md) before starting.
## Baseline
```bash
python train_baseline.py
```
## Transformer
```bash
python train_transformer.py --epochs 2 --max-train 12000
```
## Calibration/evaluation
```bash
python evaluate_predictions.py --input artifacts/predictions.json
```
## Dependency-light smoke test
```bash
python run_synthetic_eval.py
```
## Tests
```bash
python -m pytest -q
```
