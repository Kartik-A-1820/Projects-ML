from __future__ import annotations
from dataclasses import dataclass, asdict
import re
from typing import Iterable
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DEFAULT_SKILLS={
 'python':['python'],'machine_learning':['machine learning','ml'],'deep_learning':['deep learning','dl'],
 'nlp':['nlp','natural language processing'],'pytorch':['pytorch','torch'],
 'transformers':['transformer','transformers','hugging face','huggingface'],
 'rag':['rag','retrieval augmented generation','retrieval-augmented generation'],
 'fastapi':['fastapi'],'docker':['docker','containerization'],'kubernetes':['kubernetes','k8s'],
 'sql':['sql','postgresql','mysql'],'mlflow':['mlflow'],'evaluation':['model evaluation','evaluation','benchmarking'],
 'observability':['observability','tracing','monitoring'],'distributed_systems':['distributed systems','distributed computing'],
 'computer_vision':['computer vision','opencv','yolo'],'vector_database':['vector database','vector db','chroma','qdrant','weaviate','milvus']}
PII_PATTERNS=[re.compile(r'\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b'),re.compile(r'\b(?:\+?\d[\d\s\-()]{7,}\d)\b'),re.compile(r'https?://\S+')]
@dataclass
class MatchResult:
    overall_score: float; lexical_score: float; skill_score: float; matched_skills: list[str]; missing_skills: list[str]; resume_skills: list[str]; job_skills: list[str]
def normalize_text(text:str)->str:
    cleaned=text.lower()
    for p in PII_PATTERNS: cleaned=p.sub(' ',cleaned)
    cleaned=re.sub(r'[^a-z0-9+#./\-\s]',' ',cleaned)
    return re.sub(r'\s+',' ',cleaned).strip()
def extract_skills(text:str, ontology=None)->list[str]:
    ontology=ontology or DEFAULT_SKILLS; normalized=normalize_text(text); found=[]
    for canonical,aliases in ontology.items():
        if any(re.search(rf'(?<!\w){re.escape(a.lower())}(?!\w)',normalized) for a in aliases): found.append(canonical)
    return sorted(set(found))
def lexical_similarity(resume_text:str,job_text:str)->float:
    docs=[normalize_text(resume_text),normalize_text(job_text)]; v=TfidfVectorizer(ngram_range=(1,2),min_df=1,sublinear_tf=True); m=v.fit_transform(docs); return float(cosine_similarity(m[0:1],m[1:2])[0,0])
def skill_coverage(resume_skills:Iterable[str],job_skills:Iterable[str])->float:
    r,j=set(resume_skills),set(job_skills); return 1.0 if not j else len(r&j)/len(j)
def match_resume_to_job(resume_text:str,job_text:str,lexical_weight:float=0.55,skill_weight:float=0.45)->MatchResult:
    if lexical_weight<0 or skill_weight<0 or lexical_weight+skill_weight==0: raise ValueError('invalid weights')
    total=lexical_weight+skill_weight; lexical_weight/=total; skill_weight/=total
    rs,js=extract_skills(resume_text),extract_skills(job_text); lex=lexical_similarity(resume_text,job_text); cov=skill_coverage(rs,js)
    return MatchResult(round(lexical_weight*lex+skill_weight*cov,4),round(lex,4),round(cov,4),sorted(set(rs)&set(js)),sorted(set(js)-set(rs)),rs,js)
def result_to_dict(result:MatchResult)->dict: return asdict(result)
