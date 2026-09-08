class VisualMemory:
    def __init__(self): self.entries=[]
    def add(self,tool,observation):
        self.entries.append({"tool":tool,"observation":observation})
    def retrieve(self,kind=None):
        if kind is None:return list(self.entries)
        return [e for e in self.entries if e["observation"]["type"]==kind]
