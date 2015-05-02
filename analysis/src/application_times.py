import seaborn as sns

from analysis_module import AnalysisModule

class ApplicationTimes(AnalysisModule):
    def __init__(self):
        self._name = 'ApplicationTimes'
        AnalysisModule.__init__(self)
        
    def analyze(self, train_data, test_data, models):
        self.data = train_data

    def plot(self, prefix, suffix):
        keys = ['application', 'coloc', 'nice']
        plots = []
        for (app, coloc, nice), group in self.data.groupby(keys):
            sns.stripplot(x='time', hue=['coloc', 'nice'], data=group, jitter=True)
        plt.savefig('%s_app_times.%s' % (prefix, suffix))

