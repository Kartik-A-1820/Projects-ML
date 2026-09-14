class EventAggregator:
    def __init__(self,min_consecutive_positive=2,max_gap=1):
        self.min_consecutive_positive=min_consecutive_positive
        self.max_gap=max_gap
        self.run=0; self.gap=0; self.active=False

    def update(self,is_positive:bool):
        if is_positive:
            self.run+=1; self.gap=0
        else:
            self.gap+=1
            if self.gap>self.max_gap:
                self.run=0; self.active=False
        if self.run>=self.min_consecutive_positive:
            self.active=True
        return self.active
