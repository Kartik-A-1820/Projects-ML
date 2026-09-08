import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/"src"))
from graphrag_enterprise.engine import GraphRAG
e=GraphRAG()
for q in [
 "what database stores Atlas transactional metadata",
 "which ERP receives Orion work orders",
 "what infrastructure constraint applies to the plant that operates the service consuming Atlas results"
]:
    r=e.search(q);print(q,"=>",r["route"],round(r["complexity"],2),[x["id"] for x in r["hits"]])
