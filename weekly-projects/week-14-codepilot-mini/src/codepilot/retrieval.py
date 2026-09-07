from __future__ import annotations
from collections import Counter
import math,re
from .index import CodeFile

TOK=re.compile(r"[a-z_][a-z0-9_]+")

def tokens(text): return TOK.findall(text.lower())

class RepositoryRetriever:
    def __init__(self,files:list[CodeFile]):
        self.files=files
        self.docs=[tokens(f.path+" "+" ".join(f.symbols)+" "+f.text) for f in files]
        self.freq=[Counter(x) for x in self.docs]
        self.lengths=[len(x) for x in self.docs]
        self.avg=max(1,sum(self.lengths)/max(1,len(files)))
        self.df=Counter()
        for d in self.docs:self.df.update(set(d))

    def search(self,issue,top_k=5):
        q=tokens(issue); n=len(self.files); rows=[]
        for i,f in enumerate(self.files):
            score=0.; dl=self.lengths[i]
            for term in q:
                tf=self.freq[i].get(term,0)
                if not tf:continue
                idf=math.log(1+(n-self.df[term]+.5)/(self.df[term]+.5))
                score += idf*(tf*2.5)/(tf+1.5*(.25+.75*dl/self.avg))
            joined=(f.path+" "+" ".join(f.symbols)).lower()
            score += 0.35*sum(1 for t in set(q) if t in joined)
            if score>0: rows.append((float(score),f))
        rows.sort(key=lambda x:(-x[0],x[1].path))
        return rows[:top_k]

def select_context(hits,budget_chars=9000):
    selected=[];used=0
    for score,f in hits:
        block=f"FILE: {f.path}\nSYMBOLS: {', '.join(f.symbols)}\n{f.text}\n"
        if selected and used+len(block)>budget_chars: break
        selected.append((score,f)); used+=len(block)
    return selected
