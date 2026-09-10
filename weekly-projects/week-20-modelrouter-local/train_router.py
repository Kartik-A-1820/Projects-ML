import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT/"src"))
from modelrouter.core import load_rows,MarginalGainRouter
rows=load_rows();r=MarginalGainRouter().fit(rows);print("trained lightweight marginal-gain router on",len(rows),"rows")
