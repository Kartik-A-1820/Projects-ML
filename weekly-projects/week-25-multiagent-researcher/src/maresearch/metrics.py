def evidence_coverage(evidence_ids,evidence_by_id,required_topics):
    topics={evidence_by_id[i]["topic"] for i in evidence_ids if i in evidence_by_id};req=set(required_topics)
    return len(topics&req)/max(1,len(req))
def efficiency_score(coverage,messages):return coverage/max(1,messages)
