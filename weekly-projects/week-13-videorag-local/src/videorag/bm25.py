from collections import Counter
import math, re

TOKEN = re.compile(r"[a-z0-9_.:/+-]+")

def tokenize(text):
    return TOKEN.findall(text.lower())

class BM25:
    def __init__(self, documents):
        self.docs = list(documents)
        self.tokens = [tokenize(x) for x in self.docs]
        self.freq = [Counter(x) for x in self.tokens]
        self.lengths = [len(x) for x in self.tokens]
        self.avgdl = max(1.0, sum(self.lengths)/max(1,len(self.lengths)))
        self.df = Counter()
        for t in self.tokens:
            self.df.update(set(t))

    def search(self, query, top_k=5):
        q = tokenize(query)
        n = len(self.docs)
        rows = []
        for i, freq in enumerate(self.freq):
            score = 0.0
            dl = self.lengths[i]
            for term in q:
                tf = freq.get(term, 0)
                if not tf:
                    continue
                df = self.df.get(term, 0)
                idf = math.log(1 + (n-df+0.5)/(df+0.5))
                score += idf * (tf*2.5)/(tf + 1.5*(0.25+0.75*dl/self.avgdl))
            if score > 0:
                rows.append((float(score), i))
        rows.sort(key=lambda x:(-x[0],x[1]))
        return rows[:top_k]
