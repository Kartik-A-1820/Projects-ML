import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/"src"))
from agenticrag.retrieval import BM25
from agenticrag.control import CorrectiveRAG

docs=json.loads(Path("data/knowledge.json").read_text())
agent=CorrectiveRAG(BM25(docs))
for q in ["error 104 keeps happening","what does out of memory pod mean","quantum banana protocol"]:
    r=agent.run(q)
    print(q,"=>",r["status"],[x["id"] for x in r["hits"]],"steps",len(r["trace"]))
