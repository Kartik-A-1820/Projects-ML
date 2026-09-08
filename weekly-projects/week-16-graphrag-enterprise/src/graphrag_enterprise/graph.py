from collections import defaultdict, deque

class KnowledgeGraph:
    def __init__(self, triples):
        self.adj=defaultdict(list)
        for s,r,o in triples:
            self.adj[s].append((r,o))
            self.adj[o].append((f"inverse:{r}",s))
    def nodes(self): return list(self.adj)
    def traverse(self,seeds,hops=2):
        q=deque((s,0,[s]) for s in seeds if s in self.adj)
        seen=set(); paths=[]
        while q:
            node,depth,path=q.popleft()
            if (node,depth) in seen: continue
            seen.add((node,depth))
            if depth>=hops: continue
            for rel,nxt in self.adj[node]:
                p=path+[rel,nxt]; paths.append(p)
                q.append((nxt,depth+1,p))
        return paths
