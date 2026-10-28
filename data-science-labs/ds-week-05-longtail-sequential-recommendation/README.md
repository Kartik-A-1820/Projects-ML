# DS Week 05 — Long-tail sequential recommendation

A runnable reconstruction of the missing laboratory implementation. The original
repository had a dataset specification, metric tests, and a synthetic metrics
file, but no implementation or README. Matching source was not recovered during
maintenance. This version implements the documented protocol; it does not claim
to reproduce the old numbers.

## Run

Python 3.10+, CPU only:

```bash
cd data-science-labs/ds-week-05-longtail-sequential-recommendation
python -m venv .venv
# Activate .venv, then:
pip install -r requirements.txt
python -m pytest -q
python run_lab.py --output artifacts/maintenance_smoke.json
```

The default is a seeded synthetic smoke experiment with 100 users/100 items.
`artifacts/maintenance_smoke.json` is its measured output, explicitly labeled
`SYNTHETIC_SMOKE_RECONSTRUCTION`. The pre-existing `artifacts/metrics.json`
remains historical; its 700-user numbers came from unavailable source and are
not validated by the reconstruction.

For MovieLens 1M, manually obtain the dataset from GroupLens, review its terms,
then extract `ratings.dat` to `dataset/ml-1m/`:

```bash
python run_lab.py --ratings dataset/ml-1m/ratings.dat --output artifacts/movielens_results.json
```

No automatic download occurs. A MovieLens benchmark has **not** been run. The
report records a SHA-256 digest of the supplied ratings file. An optional
notebook in `notebooks/` calls the same implementation; install Jupyter separately
if using it.

## Protocol and methods

- Ratings >=4 are positives. Keep the first positive for each user/item; repeat
  consumption is out of scope. Users need at least five unique positive items.
- Sort by timestamp (item ID breaks ties). Earlier positives train, penultimate
  validates, last tests. Test context additionally includes the observed
  validation item; fitted parameters still use training histories only.
- Train-only catalog, popularity, transition counts, BPR factors, and tail
  definitions. Cold held-out items stay in the denominator and count as misses.
- Rank the full training catalog excluding seen context; no sampled-negative
  evaluation. BPR negatives exclude training positives only, not future labels.
- Compare popularity, first-order Markov transitions with popularity tie-breaking,
  NumPy BPR matrix factorization, and BPR plus an explicit tail-score bonus.
- Report Recall@K, MRR@K, single-target NDCG@K, catalog coverage, tail exposure,
  cold-target counts, and 200-resample user-bootstrap NDCG intervals.
- Define head as the top 20% of training items by count, tail as the remaining
  items. The score bonus changes exposure and can reduce accuracy; it is not a
  causal correction for exposure bias.

Choose hyperparameters using validation, then freeze them for a test report.
The smoke run's defaults are fixed, not tuned to test results. Per-user chronology
is not a globally time-censored deployment simulation: other users' training
records may occur after a given evaluation timestamp. Add a global temporal
cutoff if making real-time deployment claims. Movie ratings are preference
proxies; item exposure and counterfactual outcomes are unobserved.

## Files and validation

- `run_lab.py`: data loading, temporal split, experiment and reports.
- `src/metrics.py`: the API required by the original metric tests.
- `src/recommender.py`: train-only baselines and BPR SGD.
- `tests/`: metric examples, train/test isolation, deterministic smoke results,
  empty-input behavior, and fully observed catalog handling.
- `architecture.md`: components, tradeoffs, and scale-up boundaries.

Five tests pass locally. Synthetic results validate the pipeline, not superiority
over a baseline or MovieLens performance. BPR here is an untuned reference model;
Markov transitions provide the sequential component.

References: [MovieLens 1M](https://grouplens.org/datasets/movielens/1m/),
[BPR (Rendle et al., 2009)](https://proceedings.mlr.press/r7/rendle09a.html).
