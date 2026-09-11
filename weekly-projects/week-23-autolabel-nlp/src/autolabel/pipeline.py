from .labelers import all_votes
from .aggregate import aggregate
from .active import review_score,select_for_review

def label_rows(items,min_confidence=.68,review_budget=10):
    out=[]
    for item in items:
        votes=all_votes(item['text']); agg=aggregate(votes,min_confidence)
        out.append({**item,'votes':votes,**agg,'review_score':review_score(agg)})
    return out,select_for_review(out,review_budget)
