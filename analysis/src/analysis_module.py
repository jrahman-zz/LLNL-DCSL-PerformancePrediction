

class AnalysisModule:
    def __init__(self):
        pass

    def __str__(self):
        return self._name

    def plot_all(self, prefix, suffixes):
        for suffix in suffixes:
            self.plot(prefix, suffix)
