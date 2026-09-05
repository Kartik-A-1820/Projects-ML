from collections import Counter
import math, re
TOK=re.compile(r"[a-z0-9_./:+-]+")

def tokens(t): return TOK.findall(t.lower())

class BM25:
    def __init__(self, docs):
        self.docs=docs
        self.ts=[tokens(d["title"]+" "+d["text"]) for d in docs]
        self.freq=[Counter(x) for x in self.ts]
        self.avg=sum(map(len,self.ts))/len(self.ts)
        self.df=Counter()
        for x in self.ts: self.df.update(set(x))

    def search(self,q,k=4):
        qt=tokens(q); n=len(self.docs); rows=[]
        for i,d in enumerate(self.docs):
            score=0.0; dl=len(self.ts[i])
            for term in qt:
                tf=self.freq[i].get(term,0)
                if not tf: continue
                idf=math.log(1+(n-self.df[term]+.5)/(self.df[term]+.5))
                score += idf*(tf*2.5)/(tf+1.5*(.25+.75*dl/self.avg))
            if score>0: rows.append((score,d))
        rows.sort(key=lambda x:(-x[0],x[1]["id"]))
        return rows[:k]
