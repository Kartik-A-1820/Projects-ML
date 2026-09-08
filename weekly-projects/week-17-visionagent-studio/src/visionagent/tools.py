class ToolRegistry:
    def __init__(self):
        self.tools={}
    def register(self,name,fn): self.tools[name]=fn
    def run(self,name,scene,query):
        if name not in self.tools: raise KeyError(name)
        return self.tools[name](scene,query)

def detect_objects(scene,query):
    return {"type":"objects","items":scene.get("objects",[]),"confidence":0.95}

def read_text(scene,query):
    return {"type":"ocr","items":scene.get("text",[]),"confidence":0.98}

def spatial_relation(scene,query):
    objs=scene.get("objects",[])
    if len(objs)<2:return {"type":"spatial","items":[],"confidence":0.2}
    a,b=objs[0],objs[1]
    rel=[]
    if a["x"]<b["x"]:rel.append(f'{a["name"]} is left of {b["name"]}')
    if a["y"]<b["y"]:rel.append(f'{a["name"]} is above {b["name"]}')
    if a["y"]>b["y"]:rel.append(f'{a["name"]} is below {b["name"]}')
    return {"type":"spatial","items":rel,"confidence":0.9}
