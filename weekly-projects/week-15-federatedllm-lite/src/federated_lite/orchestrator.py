from __future__ import annotations
import random
import numpy as np
import torch
from .client import train_client
from .data import TextDataset, load_rows, stratified_holdout, non_iid_partition
from .evaluation import evaluate
from .model import TinyTextModel, adapter_state, trainable_parameter_count
from .server import weighted_fedavg
from .tokenizer import HashTokenizer

def resolve_device(value): return torch.device("cuda" if value == "auto" and torch.cuda.is_available() else ("cpu" if value == "auto" else value))
def set_seed(seed):
    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed)
    if torch.cuda.is_available(): torch.cuda.manual_seed_all(seed)

def run_simulation(cfg, rounds_override=None, privacy_override=None):
    seed=int(cfg["seed"]); set_seed(seed); device=resolve_device(cfg.get("device","auto"))
    rows=load_rows("data/messages.json")
    train_rows,val_rows=stratified_holdout(rows,cfg["data"]["validation_fraction"],seed)
    tokenizer=HashTokenizer(vocab_size=cfg["model"]["vocab_size"])
    client_rows=non_iid_partition(train_rows,cfg["data"]["num_clients"],cfg["data"]["non_iid_alpha"],seed)
    client_datasets=[TextDataset(r,tokenizer) for r in client_rows]; val_dataset=TextDataset(val_rows,tokenizer)
    model=TinyTextModel(vocab_size=cfg["model"]["vocab_size"],embedding_dim=cfg["model"]["embedding_dim"],hidden_dim=cfg["model"]["hidden_dim"],num_classes=cfg["model"]["num_classes"],lora_rank=cfg["model"]["lora_rank"],lora_alpha=cfg["model"]["lora_alpha"])
    global_adapter=adapter_state(model); rounds=rounds_override or cfg["training"]["rounds"]
    privacy_enabled=cfg["privacy"]["enabled"] if privacy_override is None else privacy_override
    history=[]
    for rnd in range(1,rounds+1):
        results=[]
        for client_id,ds in enumerate(client_datasets):
            results.append(train_client(client_id,model,global_adapter,ds,cfg["training"]["local_epochs"],cfg["training"]["batch_size"],cfg["training"]["learning_rate"],cfg["training"]["weight_decay"],device,privacy_enabled,cfg["privacy"]["max_update_norm"],cfg["privacy"]["noise_multiplier"],seed+rnd*100))
        global_adapter,stats=weighted_fedavg(global_adapter,results,cfg["aggregation"]["secure_aggregation_simulation"],seed+rnd)
        global_accuracy=evaluate(model,global_adapter,val_dataset,device)
        client_accs=[evaluate(model,global_adapter,ds,device) for ds in client_datasets]
        history.append({"round":rnd,"global_accuracy":global_accuracy,"mean_client_accuracy":float(np.mean(client_accs)),"worst_client_accuracy":float(np.min(client_accs)),"client_sizes":[len(ds) for ds in client_datasets],"mean_train_loss":float(np.mean([r.train_loss for r in results])),"mean_pre_clip_norm":float(np.mean([r.pre_clip_norm for r in results])),"mean_clip_scale":float(np.mean([r.clip_scale for r in results])),"communicated_bytes":stats.communicated_bytes})
    return {"device":str(device),"privacy_enabled":privacy_enabled,"secure_aggregation_simulated":cfg["aggregation"]["secure_aggregation_simulation"],"trainable_adapter_parameters":trainable_parameter_count(model),"rounds":history}
