import json
from pathlib import Path
from modelregistry.store import Registry
from modelregistry.lifecycle import promote,rollback
from modelregistry.demo_model import train

def create(tmp_path,C=1.0,status="passed"):
    reg=Registry(tmp_path/"r.db",tmp_path/"store")
    p=tmp_path/"m.pkl";metrics,h,sig=train(p,C=C)
    v=reg.register("m",p,sig,metrics,{"validation_status":status},h,"git-1","run-1")
    return reg,v

def test_register_and_checksum(tmp_path):
    reg,v=create(tmp_path)
    assert reg.verify_artifact("m",v)

def test_promotion_gate(tmp_path):
    reg,v=create(tmp_path,status="failed")
    policy={"required_metrics":{"accuracy":.5},"required_tags":{"validation_status":"passed"},"require_signature":True,"require_data_hash":True}
    assert not promote(reg,"m",v,policy)["promoted"]

def test_champion_alias_and_rollback(tmp_path):
    reg=Registry(tmp_path/"r.db",tmp_path/"store")
    versions=[]
    for i,C in enumerate([.2,2.0]):
        p=tmp_path/f"m{i}.pkl";metrics,h,sig=train(p,C=C)
        versions.append(reg.register("m",p,sig,metrics,{"validation_status":"passed"},h,f"g{i}",f"r{i}"))
    policy={"required_metrics":{"accuracy":.5},"required_tags":{"validation_status":"passed"},"require_signature":True,"require_data_hash":True}
    assert promote(reg,"m",versions[0],policy)["promoted"]
    assert promote(reg,"m",versions[1],policy)["promoted"]
    assert reg.resolve_alias("m","champion")["version"]==versions[1]
    rb=rollback(reg,"m")
    assert rb["champion"]==versions[0]

def test_audit_history(tmp_path):
    reg,v=create(tmp_path)
    assert reg.audit_events("m")[0][0]=="register"
