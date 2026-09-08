from pathlib import Path
import yaml
import torch
from federated_lite.data import load_rows,stratified_holdout,non_iid_partition
from federated_lite.model import TinyTextModel,trainable_parameter_count
from federated_lite.privacy import clip_update,l2_norm
from federated_lite.secure_agg import apply_canceling_masks
from federated_lite.orchestrator import run_simulation

def test_partition_preserves_all_rows():
    rows=load_rows("data/messages.json"); train,_=stratified_holdout(rows,0.25,42); clients=non_iid_partition(train,4,0.35,42)
    assert sum(len(c) for c in clients)==len(train) and all(len(c)>0 for c in clients)

def test_only_lora_parameters_are_trainable():
    model=TinyTextModel(); names=[n for n,p in model.named_parameters() if p.requires_grad]
    assert names and all("lora_" in n for n in names) and trainable_parameter_count(model)<sum(p.numel() for p in model.parameters())

def test_clip_update_respects_norm():
    clipped,before,scale=clip_update({"x":torch.tensor([3.0,4.0])},1.0)
    assert abs(before-5.0)<1e-6 and l2_norm(clipped)<=1.000001 and scale<1.0

def test_secure_masks_cancel():
    d1={"x":torch.tensor([1.0,2.0])}; d2={"x":torch.tensor([3.0,4.0])}; masked=apply_canceling_masks([d1,d2],7)
    assert torch.allclose(masked[0]["x"]+masked[1]["x"],d1["x"]+d2["x"])

def test_smoke_simulation():
    cfg=yaml.safe_load(Path("configs/config.yaml").read_text()); cfg["training"]["rounds"]=1; cfg["privacy"]["noise_multiplier"]=0.0
    result=run_simulation(cfg); assert result["rounds"] and 0<=result["rounds"][0]["global_accuracy"]<=1 and result["rounds"][0]["communicated_bytes"]>0
