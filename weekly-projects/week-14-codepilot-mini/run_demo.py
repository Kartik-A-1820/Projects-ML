import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/"src"))
from codepilot.index import scan_repository
from codepilot.retrieval import RepositoryRetriever,select_context
from codepilot.planning import build_plan

issue="discount larger than subtotal can create a negative order total; clamp total at zero and add a regression test"
files=scan_repository("sample_repo")
hits=RepositoryRetriever(files).search(issue,5)
context=select_context(hits,6000)
print("retrieved",[(round(s,3),f.path) for s,f in context])
print(json.dumps(build_plan(issue,context),indent=2))
