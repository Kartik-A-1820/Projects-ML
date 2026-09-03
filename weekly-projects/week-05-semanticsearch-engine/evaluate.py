import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from semantic_search.engine import SearchEngine, load_documents
from semantic_search.metrics import ndcg_at_k, recall_at_k, reciprocal_rank


engine = SearchEngine(load_documents("data/documents.json"))
queries = json.loads(Path("data/eval_queries.json").read_text(encoding="utf-8"))

rows = []
for item in queries:
    hits = engine.search(item["query"], top_k=5)
    ranked = [h.doc_id for h in hits]
    relevant = set(item["relevant"])
    rows.append({
        "query": item["query"],
        "recall@5": recall_at_k(ranked, relevant, 5),
        "mrr": reciprocal_rank(ranked, relevant),
        "ndcg@5": ndcg_at_k(ranked, relevant, 5),
    })

for row in rows:
    print(row)

print("mean_ndcg@5=", round(sum(x["ndcg@5"] for x in rows) / len(rows), 4))
