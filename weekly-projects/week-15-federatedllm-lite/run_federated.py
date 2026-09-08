from __future__ import annotations
import argparse, json, sys
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/"src"))
from federated_lite.orchestrator import run_simulation

def main():
    p=argparse.ArgumentParser(); p.add_argument("--config",default="configs/config.yaml"); p.add_argument("--rounds",type=int,default=None); p.add_argument("--no-privacy",action="store_true"); a=p.parse_args()
    cfg=yaml.safe_load(Path(a.config).read_text(encoding="utf-8"))
    result=run_simulation(cfg,rounds_override=a.rounds,privacy_override=False if a.no_privacy else None)
    print(json.dumps(result,indent=2))
if __name__=="__main__": main()
