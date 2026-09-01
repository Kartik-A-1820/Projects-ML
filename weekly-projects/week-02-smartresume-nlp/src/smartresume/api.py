from fastapi import FastAPI
from pydantic import BaseModel, Field
from .core import match_resume_to_job, result_to_dict
class MatchRequest(BaseModel):
    resume_text: str = Field(min_length=20)
    job_text: str = Field(min_length=20)
app=FastAPI(title='SmartResume-NLP',version='1.0.0')
@app.get('/health')
def health(): return {'status':'ok'}
@app.post('/match')
def match(request:MatchRequest): return result_to_dict(match_resume_to_job(request.resume_text,request.job_text))
