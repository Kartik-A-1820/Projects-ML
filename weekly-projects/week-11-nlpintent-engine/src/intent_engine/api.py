from fastapi import FastAPI
from pydantic import BaseModel, Field
from .io import load_rows
from .model import IntentClassifier

class Request(BaseModel):
    text: str = Field(min_length=2)

app=FastAPI(title='NLPIntent-Engine',version='1.0.0')
rows=load_rows('data/intents.json')
clf=IntentClassifier(oos_threshold=0.19,ambiguity_margin=0.01,similarity_threshold=0.05).fit([r['text'] for r in rows],[r['intent'] for r in rows])

@app.get('/health')
def health(): return {'status':'ok'}

@app.post('/intent')
def intent(req:Request): return clf.predict_one(req.text).__dict__
