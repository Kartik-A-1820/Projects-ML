def choose_tools(query):
    q=query.lower(); tools=[]
    if any(w in q for w in ["text","read","word","label","alert","number"]):tools.append("ocr")
    if any(w in q for w in ["left","right","above","below","where","relation"]):tools.extend(["objects","spatial"])
    if any(w in q for w in ["object","shape","color","see"]):tools.append("objects")
    if not tools:tools=["objects","ocr"]
    return list(dict.fromkeys(tools))
