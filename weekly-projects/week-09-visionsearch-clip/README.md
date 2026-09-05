# Week 09 — VisionSearch-CLIP (2026 Rebuild)

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
- production scaling architecture

## Hardware
Ryzen 7 4800-series CPU, 16 GB RAM, GTX 1650 Ti 4 GB.
Use CPU for small corpora or a small encoder on the GTX 1650 Ti. Do not use the largest So400M variants locally.

## Run
```bash
pip install -r requirements.txt
python run_demo.py
pytest -q
```

## Optional real embeddings
Install the optional transformer dependencies and select a small SigLIP 2 checkpoint in `configs/config.yaml`.

## Resume bullet
Built a multimodal retrieval engine for cross-modal text↔image search with normalized open vision-language embeddings, metadata-aware ranking, duplicate controls and Recall/MRR evaluation; designed production scaling for batched GPU embedding, vector sharding, model/index lineage, multimodal observability and tenant-isolated retrieval.
