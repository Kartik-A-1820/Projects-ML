from dataclasses import dataclass
import time
@dataclass
class Entry:
    key:str; query:str; response:str; vector:object; created_at:float; ttl:int; tenant:str; model_version:str; prompt_version:str; curated:bool=False
class CacheStore:
    def __init__(self): self.entries={}
    def put(self,e): self.entries[e.key]=e
    def values(self): return list(self.entries.values())
    def expired(self,e,now=None): return (now or time.time())-e.created_at>e.ttl
