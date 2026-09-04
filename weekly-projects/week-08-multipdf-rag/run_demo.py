import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT/'src'))
from multipdf_rag.engine import Engine
q=' '.join(sys.argv[1:]) or 'What does AC-17 require?'; print(Engine(['data/policies.txt','data/platform.txt']).query(q))
