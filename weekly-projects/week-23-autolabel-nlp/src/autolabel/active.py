def review_score(agg):
    # disagreement and uncertainty prioritize review
    return float((1-agg['confidence']) + agg['entropy'])
def select_for_review(rows,budget=10):
    return sorted(rows,key=lambda x:(-x['review_score'],x['text']))[:budget]
