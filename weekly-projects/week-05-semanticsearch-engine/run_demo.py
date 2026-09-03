import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from semantic_search.engine import SearchEngine, load_documents


query = " ".join(sys.argv[1:]) or "hybrid semantic keyword search"
engine = SearchEngine(load_documents("data/documents.json"))
for rank, hit in enumerate(engine.search(query, top_k=5), start=1):
    print(rank, hit.doc_id, round(hit.score, 4), hit.title)
