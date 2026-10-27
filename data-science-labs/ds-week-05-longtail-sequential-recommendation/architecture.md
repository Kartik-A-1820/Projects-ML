# Architecture

Timestamped ratings → positive filtering/deduplication → per-user leave-last-two
split → train-only catalog/statistics/BPR → full-catalog ranking → validation/test
metrics and provenance report.

`run_lab.py` owns splitting and experimental policy. `src/recommender.py` sees
only training histories; it never sees held-out labels during fitting or negative
sampling. `src/metrics.py` is dependency-light and supports the original tests.
The notebook calls these modules rather than maintaining a second implementation.

The CPU NumPy implementation favors inspectability over throughput. For large
catalogs, move BPR SGD to vectorized/GPU training, evaluate retrieval candidate
recall separately from reranking, persist model/data fingerprints, and use a
bounded candidate stage. Those are proposed extensions, not implemented serving
features. Add source/user privacy controls for production interaction logs.

Evaluation assumes per-user chronological preference prediction over a fixed
training catalog. It cannot establish counterfactual exposure fairness, globally
causal time validity, or quality for entirely new users/items. Tail exposure and
accuracy must be considered jointly; the smoke report can favor popularity on
accuracy while a tail bonus increases exposure.
