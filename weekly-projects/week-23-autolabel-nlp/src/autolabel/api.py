from fastapi import FastAPI
from pydantic import BaseModel
from .pipeline import label_rows
class Req(BaseModel): text:str
app=FastAPI(title='AutoLabel-NLP',version='1.0.0')
@app.get('/health')
def health():return {'status':'ok'}
@app.post('/label')
def label(r:Req):return label_rows([{'text':r.text}],review_budget=1)[0][0]
