from llmcache.store import CacheStore
from llmcache.policy import SemanticCache,key_for,freshness_risk
from llmcache.embedding import similarity

def test_exact_hit():
 s=CacheStore();c=SemanticCache(s);c.insert('hello','world');assert c.lookup('hello')['status']=='exact_hit'
def test_tenant_isolation():
 s=CacheStore();c=SemanticCache(s,hit_threshold=.1);c.insert('reset password','x',tenant='a');assert c.lookup('reset password',tenant='b')['status']=='miss'
def test_semantic_similarity(): assert similarity('refund missing','reimbursement missing')>0
def test_verify_band():
 s=CacheStore();c=SemanticCache(s,hit_threshold=.99,verify_lower_bound=.1);c.insert('reset password','x');assert c.lookup('forgot password')['status'] in {'verify_candidate','miss'}
def test_freshness_risk_increases():
 s=CacheStore();c=SemanticCache(s);k=c.insert('x','y',now=1000);e=s.entries[k];assert freshness_risk(e,4600) > freshness_risk(e,1001)
