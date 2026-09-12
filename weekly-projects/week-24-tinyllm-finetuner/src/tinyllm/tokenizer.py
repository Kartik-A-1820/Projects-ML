import hashlib,re,torch
TOK=re.compile(r"[a-z0-9_]+")
class HashTokenizer:
    def __init__(self,vocab_size=512,max_length=20):
        self.vocab_size=vocab_size;self.max_length=max_length
    def encode(self,text):
        ids=[]
        for t in TOK.findall(text.lower())[:self.max_length]:
            h=int(hashlib.sha256(t.encode()).hexdigest()[:8],16)
            ids.append(2+h%(self.vocab_size-2))
        ids=ids or [1]
        ids += [0]*(self.max_length-len(ids))
        return torch.tensor(ids,dtype=torch.long)
