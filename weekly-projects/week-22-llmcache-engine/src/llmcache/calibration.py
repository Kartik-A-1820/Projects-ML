from .embedding import similarity
def choose_threshold(pairs,target_precision=.95):
    scored=sorted([(similarity(x['a'],x['b']),bool(x['same'])) for x in pairs],reverse=True)
    best=1.0
    for threshold,_ in scored:
        chosen=[y for s,y in scored if s>=threshold]
        if chosen and sum(chosen)/len(chosen)>=target_precision: best=min(best,threshold)
    return best
