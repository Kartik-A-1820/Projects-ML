def answerable_accuracy(results, expected):
    return sum((r["status"]=="grounded")==e for r,e in zip(results,expected))/len(expected)

def mean_steps(results):
    return sum(len(r["trace"]) for r in results)/len(results)
