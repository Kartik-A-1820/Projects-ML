import json,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/"src"))
from modelregistry.demo_model import train
from modelregistry.store import Registry
from modelregistry.lifecycle import promote,rollback

policy=json.loads(Path("configs/promotion_policy.json").read_text())
with tempfile.TemporaryDirectory() as td:
    t=Path(td);reg=Registry(t/"registry.db",t/"store")
    for i,C in enumerate([.2,2.0],1):
        model=t/f"m{i}.pkl";metrics,data_hash,signature=train(model,C=C)
        v=reg.register("iris-risk",model,signature,metrics,{"validation_status":"passed"},data_hash,f"git-demo-{i}",f"run-{i}")
        print("registered",v,metrics,reg.verify_artifact("iris-risk",v))
        print("promotion",promote(reg,"iris-risk",v,policy))
    print("champion",reg.resolve_alias("iris-risk","champion")["version"])
    print("rollback",rollback(reg,"iris-risk"))
    print("audit",reg.audit_events("iris-risk"))
