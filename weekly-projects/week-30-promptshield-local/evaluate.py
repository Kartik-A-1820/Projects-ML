import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT/"src"))
from promptshield.policy import PolicyEngine
from promptshield.gateway import SecureToolGateway
cases=json.loads((ROOT/"sample_data/attacks.json").read_text())
g=SecureToolGateway(PolicyEngine(ROOT/"configs/policy.yaml"))
expected={"indirect_web_injection":False,"path_escape":False,"benign_search":True}
rows=[]
for x in cases:
    r=g.request(x["name"],x["objective"],x["tool"]["name"],x["tool"]["args"],x["observation"])
    rows.append((x["name"],r["allowed"],expected[x["name"]]))
acc=sum(a==e for _,a,e in rows)/len(rows)
print({"policy_accuracy":acc,"cases":rows})
