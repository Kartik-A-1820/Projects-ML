# DATASET.md

Source: GroupLens MovieLens 1M: https://grouplens.org/datasets/movielens/1m/

Download ml-1m.zip from GroupLens and extract ratings.dat and movies.dat into dataset/ml-1m/. Review the accompanying GroupLens README/license terms. Raw data is intentionally not committed.

Target: next positive item, with ratings >=4 treated as positive preference signals.
Split: leave-last-two per user: earlier positives=train, penultimate=validation, last=test.
Leakage: all popularity, transition and representation statistics must use training history only.
Synthetic fallback: deterministic timestamped sequences for code verification only; not a MovieLens benchmark.