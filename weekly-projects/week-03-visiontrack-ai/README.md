# Week 03 — VisionTrack-AI
Local-first multi-object video analytics for edge hardware. The design separates detection, tracking, and event analytics so the core is testable without model downloads while real video mode can use the configured YOLO26n detector adapter.
## Capabilities
- optional YOLO26 nano detector adapter
- deterministic IoU multi-object tracker
- persistent track IDs and bounded trajectory history
- line-crossing events and per-class counts
- JSONL event export
- local CPU tracking + GPU detector split
- proposed deployment architecture notes
## Hardware target
Ryzen 7 4800-series CPU, 16 GB RAM, GTX 1650 Ti 4 GB VRAM.
Run commands from this lab's directory in an activated, isolated environment. See the [setup and contribution guide](../../CONTRIBUTING.md) before starting.
## Run deterministic smoke demo
```bash
python run_synthetic.py
```
## Run real video
```bash
python -m pip install -r requirements.txt
python run_video.py --source input.mp4 --model yolo26n.pt
```
## Tests
```bash
python -m pytest -q
```
