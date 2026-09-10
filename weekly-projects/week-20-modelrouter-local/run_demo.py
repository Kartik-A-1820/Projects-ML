import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT/"src"))
from modelrouter.core import load_rows,MarginalGainRouter,ModelRouter
r=ModelRouter(learned=MarginalGainRouter().fit(load_rows()))
for q in ["rewrite this email politely","write a regex for an ISO date","design a multi region agent architecture with DR and security","debug a race condition across async workers"]:print(q,"=>",r.route(q))
