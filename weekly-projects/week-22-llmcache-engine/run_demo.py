import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT/'src'))
from llmcache.store import CacheStore
from llmcache.policy import SemanticCache
s=CacheStore();c=SemanticCache(s,hit_threshold=.45,verify_lower_bound=.2);c.insert('reset my password','Use account recovery',curated=True)
for q in ['reset my password','help me reset forgotten password','track shipment']:
 print(q,'=>',c.lookup(q))
