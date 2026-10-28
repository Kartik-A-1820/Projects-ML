"""Train-only popularity, sequential transitions, and NumPy BPR baselines."""
from collections import Counter, defaultdict
import numpy as np

class Recommenders:
    def __init__(self, histories, seed=42, dimensions=16, epochs=3):
        self.histories = histories
        self.users = sorted(histories)
        self.items = sorted({item for history in histories.values() for item in history})
        self.item_index = {item:i for i,item in enumerate(self.items)}
        self.user_index = {user:i for i,user in enumerate(self.users)}
        self.counts = Counter(item for history in histories.values() for item in history)
        self.popularity_denominator = 1 + sum(self.counts.values())
        self.transitions = defaultdict(Counter)
        for history in histories.values():
            for previous, following in zip(history, history[1:]):
                self.transitions[previous][following] += 1
        ordered = sorted(self.items, key=lambda item: (-self.counts[item], item))
        n_head = max(1, int(np.ceil(.2 * len(ordered))))
        self.tail = set(ordered[n_head:])
        rng = np.random.default_rng(seed)
        self.user_factors = rng.normal(0,.05,(len(self.users),dimensions))
        self.item_factors = rng.normal(0,.05,(len(self.items),dimensions))
        positives = {user:{self.item_index[item] for item in history} for user,history in histories.items()}
        pairs = [(self.user_index[user],self.item_index[item],user) for user,history in histories.items() for item in history if len(positives[user]) < len(self.items)]
        if not pairs:
            return
        for _ in range(epochs * len(pairs)):
            u,i,user = pairs[rng.integers(len(pairs))]
            j = int(rng.integers(len(self.items)))
            attempts=0
            while j in positives[user]:
                attempts+=1
                if attempts>50:
                    j=int(rng.choice(sorted(set(range(len(self.items)))-positives[user])))
                    break
                j=int(rng.integers(len(self.items)))
            user_vector=self.user_factors[u].copy()
            pos,neg=self.item_factors[i].copy(),self.item_factors[j].copy()
            gradient=1./(1.+np.exp(np.clip(user_vector@(pos-neg),-30,30)))
            self.user_factors[u]+=.03*(gradient*(pos-neg)-.01*user_vector)
            self.item_factors[i]+=.03*(gradient*user_vector-.01*pos)
            self.item_factors[j]+=.03*(-gradient*user_vector-.01*neg)

    def recommend(self, user, context, method, k, tail_bonus=0.):
        if k<1:
            raise ValueError('k must be positive')
        seen=set(context)
        candidates=[item for item in self.items if item not in seen]
        if method=='popularity':
            scores={item:float(self.counts[item]) for item in candidates}
        elif method=='markov':
            transitions=self.transitions[context[-1]] if context else {}
            # Train-only popularity breaks transition ties deterministically.
            scores={item:float(transitions.get(item,0)) + self.counts[item]/self.popularity_denominator for item in candidates}
        elif method in ('bpr','bpr_tail'):
            values=self.item_factors@self.user_factors[self.user_index[user]]
            scores={item:float(values[self.item_index[item]]) for item in candidates}
            if method=='bpr_tail' and candidates:
                scale=np.std(list(scores.values())) or 1.
                scores={item:value/scale + tail_bonus*(item in self.tail) for item,value in scores.items()}
        else:
            raise ValueError('Unknown recommender')
        return sorted(candidates,key=lambda item:(-scores[item],item))[:k]
