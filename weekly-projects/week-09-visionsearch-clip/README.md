# Week 09 — VisionSearch-CLIP
Local-first image/text retrieval with an **open multimodal encoder adapter**, metadata filters,
cosine retrieval, duplicate-aware evaluation and an optional modern SigLIP 2 model.
The project keeps the historical CLIP name because CLIP-style dual-encoder retrieval is the core idea,
but the preferred 2026 adapter is SigLIP 2 when hardware allows it.
## Capabilities
- deterministic offline retrieval core for tests
- optional Hugging Face SigLIP 2 adapter
- text-to-image and image-to-image search
- normalized vector index
- metadata filters
- Recall@K / MRR evaluation
- duplicate-aware indexing
- local JSON artifact store
- proposed deployment architecture notes
## Hardware
Ryzen 7 4800-series CPU, 16 GB RAM, GTX 1650 Ti 4 GB.
Use CPU for small corpora or a small encoder on the GTX 1650 Ti. Do not use the largest So400M variants locally.
Run commands from this lab's directory in an activated, isolated environment. See the [setup and contribution guide](../../CONTRIBUTING.md) before starting.
## Run
```bash
python -m pip install -r requirements.txt
python run_demo.py
python -m pytest -q
```
## Optional real embeddings
Install the optional transformer dependencies and select a small SigLIP 2 checkpoint in `configs/config.yaml`.
