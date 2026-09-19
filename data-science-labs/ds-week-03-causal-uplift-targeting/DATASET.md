# DATASET.md — Hillstrom Email Marketing Experiment

**Canonical dataset:** Kevin Hillstrom, MineThatData E-Mail Analytics and Data Mining Challenge (2008).

The experiment contains 64,000 customers randomly assigned approximately one-third each to Men's E-Mail, Women's E-Mail, or No E-Mail. Outcomes were observed over the following two weeks: visit, conversion, and spend.

## Features used
Pre-treatment only: recency, history/history segment, prior men's/women's merchandise indicators, zip code, newbie status, and historical purchase channel.

## Treatment
Primary analysis: `treatment = 1` for either email arm and `0` for No E-Mail.

## Target
`conversion`: purchase within the post-campaign observation window.

## Leakage exclusions
`visit` and `spend` are post-treatment outcomes and are never model inputs. `segment` is used only to construct treatment.

## Access
The dataset is documented by scikit-uplift (`fetch_hillstrom`) and TensorFlow Datasets (`hillstrom`). Do not commit raw data to this repository. Place a locally obtained copy at `dataset/hillstrom.csv`. The notebook detects it automatically.

## License/access note
The original challenge data is publicly distributed through the MineThatData ecosystem and mirrored by open-source dataset loaders. This repository does not redistribute it. Users should review the source terms applicable at download time.

## Synthetic fallback
When the real file is absent, the notebook generates a deterministic randomized-treatment dataset with analogous pre-treatment customer features and heterogeneous treatment effects. Synthetic results are explicitly labeled and must not be presented as Hillstrom benchmark results.
