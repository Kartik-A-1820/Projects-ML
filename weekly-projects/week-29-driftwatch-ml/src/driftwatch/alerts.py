class PersistentAlert:
    def __init__(self,persistence_windows=2,recovery_windows=2):
        self.persistence_windows=persistence_windows
        self.recovery_windows=recovery_windows
        self.bad=0; self.good=0; self.active=False

    def update(self,drifted:bool):
        if drifted:
            self.bad+=1; self.good=0
            if self.bad>=self.persistence_windows:self.active=True
        else:
            self.good+=1; self.bad=0
            if self.good>=self.recovery_windows:self.active=False
        return self.active
