from dataclasses import dataclass
from pathlib import Path
import yaml

@dataclass
class Decision:
    allowed: bool
    reason: str
    require_approval: bool=False
    risk: str="unknown"

class PolicyEngine:
    def __init__(self, policy_path):
        self.cfg=yaml.safe_load(Path(policy_path).read_text())
    def inspect_observation(self,text):
        low=text.lower()
        return [p for p in self.cfg.get("blocked_patterns",[]) if p.lower() in low]
    def authorize(self,tool,args,observation="",approved=False):
        hits=self.inspect_observation(observation)
        if hits: return Decision(False,f"untrusted_observation:{hits[0]}")
        spec=self.cfg.get("allowed_tools",{}).get(tool)
        if not spec: return Decision(False,"tool_not_allowlisted")
        extra=set(args)-set(spec.get("allowed_args",[]))
        if extra: return Decision(False,f"unexpected_args:{sorted(extra)}",risk=spec.get("risk","unknown"))
        if tool=="read_file":
            path=str(args.get("path",""))
            if not any(path.startswith(p) for p in spec.get("path_prefixes",[])):
                return Decision(False,"path_outside_scope",risk=spec.get("risk","medium"))
        if spec.get("require_approval") and not approved:
            return Decision(False,"human_approval_required",True,spec.get("risk","high"))
        return Decision(True,"policy_allow",False,spec.get("risk","low"))
