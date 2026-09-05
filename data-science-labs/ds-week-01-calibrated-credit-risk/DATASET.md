# Dataset Card — Default of Credit Card Clients

Canonical source: UCI Machine Learning Repository dataset 350, DOI `10.24432/C55S3H`.

UCI reports 30,000 instances, 23 explanatory features, a binary next-month default target, and CC BY 4.0 licensing.

Alternative mirror: Hugging Face `scikit-learn/credit-card-clients`.

```python
from ucimlrepo import fetch_ucirepo
credit = fetch_ucirepo(id=350)
X = credit.data.features.copy()
y = credit.data.targets.squeeze().astype(int)
```

Raw data is not committed. `ID` is excluded. `SEX`, `MARRIAGE`, `EDUCATION`, and `AGE` are excluded from the main model and used only for diagnostic slices. Full empirical claims must come from the real dataset, not the synthetic smoke fallback.
