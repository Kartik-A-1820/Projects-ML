# Week 03 — VisionTrack-AI (2026 Rebuild)

Local-first multi-object video analytics for edge hardware. The design separates detection, tracking, and event analytics so the core is testable without model downloads while real video mode can use a current lightweight detector such as YOLO26n.

## Capabilities
- optional YOLO26 nano detector adapter
- deterministic IoU multi-object tracker
- persistent track IDs and bounded trajectory history
- line-crossing events and per-class counts
- JSONL event export
- local CPU tracking + GPU detector split
- production scaling architecture

## Hardware target
Ryzen 7 4800-series CPU, 16 GB RAM, GTX 1650 Ti 4 GB VRAM.

## Run deterministic smoke demo
```bash
python run_synthetic.py
```

## Run real video
```bash
pip install -r requirements.txt
python run_video.py --source input.mp4 --model yolo26n.pt
```

## Tests
```bash
pytest -q
```

## Resume bullet
Built an edge-efficient multi-object video analytics pipeline with detector/tracker separation, persistent identities, trajectory and crossing analytics, auditable events, and a production path covering GPU inference pools, stream partitioning, backpressure, observability, and multi-camera scaling.
