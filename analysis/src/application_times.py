import seaborn as sns

from analysis_module import AnalysisModule

class ApplicationTimes(AnalysisModule):
    def __init__(self):
        self._name = 'ApplicationTimes'
        AnalysisModule.__init__(self)
        
    def analyze(self, train_data, test_data, models):
        keys = ['application', 'coloc', 'nice']
        plots = []
        for name, group in train_data.groupby(keys):
            app = name[0]
            coloc = name[1]
            nice = name[2]
            plots.append(sns.stripplot(x='time', hue=['coloc', 'nice'], data=group, jitter=True))
        return plots

