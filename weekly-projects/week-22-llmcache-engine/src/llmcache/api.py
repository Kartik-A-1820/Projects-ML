from fastapi import FastAPI
from pydantic import BaseModel
from .store import CacheStore
from .policy import SemanticCache
class Req(BaseModel): query:str; tenant:str='default'
store=CacheStore(); cache=SemanticCache(store); cache.insert('reset my password','Use the verified account recovery flow',curated=True)
app=FastAPI(title='LLMCache-Engine',version='1.0.0')
@app.get('/health')
def health():return {'status':'ok'}
@app.post('/lookup')
def lookup(r:Req):return cache.lookup(r.query,r.tenant)
