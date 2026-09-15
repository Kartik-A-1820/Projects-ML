import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT/"src"))
from promptshield.policy import PolicyEngine
from promptshield.gateway import SecureToolGateway
p=PolicyEngine(ROOT/"configs/policy.yaml");g=SecureToolGateway(p)
for x in json.loads((ROOT/"sample_data/attacks.json").read_text()):
    print(x["name"],g.request(x["name"],x["objective"],x["tool"]["name"],x["tool"]["args"],x["observation"]))
