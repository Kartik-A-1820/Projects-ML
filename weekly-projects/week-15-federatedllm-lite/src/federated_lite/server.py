from __future__ import annotations
from dataclasses import dataclass
from .privacy import add_states
from .secure_agg import apply_canceling_masks

@dataclass
class AggregationStats:
    total_examples: int
    communicated_bytes: int
    secure_aggregation_simulated: bool

def weighted_fedavg(global_state, client_results, secure_aggregation_simulation=True, seed=42):
    if not client_results: raise ValueError("no client results")
    total_examples = sum(r.num_examples for r in client_results)
    if secure_aggregation_simulation:
        weighted = [{k: v * (r.num_examples / total_examples) for k, v in r.delta.items()} for r in client_results]
        weighted = apply_canceling_masks(weighted, seed=seed)
        aggregate = {k: sum(d[k] for d in weighted) for k in global_state}
    else:
        aggregate = {k: sum(r.delta[k] * (r.num_examples / total_examples) for r in client_results) for k in global_state}
    new_state = add_states(global_state, aggregate)
    communicated_bytes = sum(v.numel() * v.element_size() for r in client_results for v in r.delta.values())
    return new_state, AggregationStats(total_examples, communicated_bytes, secure_aggregation_simulation)
