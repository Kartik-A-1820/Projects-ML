# Dataset card — PhiUSIIL Phishing URL (UCI ID 967)

Canonical source: https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+dataset
Direct archive: https://archive.ics.uci.edu/static/public/967/phiusiil%2Bphishing%2Burl%2Bdataset.zip
Citation: Prasad & Chandra (2024), PhiUSIIL Phishing URL (Website), UCI Machine Learning Repository; related paper DOI https://doi.org/10.1016/j.cose.2023.103545.
License: **CC BY 4.0**, credit required. Download yourself; raw data is intentionally excluded from repository.

235,795 URL/page observations; 134,850 legitimate and 100,945 phishing in the UCI description. **Original label 0 = phishing; original label 1 = legitimate**. Project `target = 1 - label`, so positive = phishing.

Download the ZIP from UCI, extract `PhiUSIIL_Phishing_URL_Dataset.csv` into `data/`. The notebook runs the REAL benchmark only when this CSV is present. Otherwise it explicitly runs a **synthetic smoke test**, not a valid estimate of phishing performance.

Scope: only `URL` and `label` are read. Webpage-content features, `URLSimilarityIndex`, `TLDLegitimateProb`, and derived website features are deliberately excluded to avoid prediction-time availability/leakage ambiguity. `Domain` is not a model feature. Hostname-derived domain groups are used for leakage-resistant splits; our root-domain heuristic covers common ccTLDs but is NOT a complete public-suffix-list implementation. For high-stakes deployment replace it with a version-pinned Public Suffix List and audit shared registrable domains. No timestamps are available; temporal generalization cannot be claimed.

Cleaning: remove invalid rows, conflicting labels for identical URLs, exact URL duplicates, then group-disjoint split. Features only use the URL string available at inference. Evaluation on a single historical public dataset cannot establish live production phishing efficacy. URL labels may be stale or noisy.