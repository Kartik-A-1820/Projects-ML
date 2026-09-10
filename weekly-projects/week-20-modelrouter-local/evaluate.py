import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT/"src"))
from modelrouter.core import load_rows,MarginalGainRouter,ModelRouter,evaluate_routes
rows=load_rows();router=ModelRouter(learned=MarginalGainRouter().fit(rows));dec=[router.route(x["query"],x).model for x in rows]
print("routes",dec);print(evaluate_routes(rows,dec,{"small":1.0,"medium":2.7,"strong":8.0}))
