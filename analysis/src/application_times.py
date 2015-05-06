import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from analysis_module import AnalysisModule

def coloc_map(coloc):
    if coloc == 0:
        return "Same core"
    elif coloc == 1:
        return "Same socket"
    else:
        return "Different socket"

def wrapper(data, *args, **kwargs):
    sns.seaborn(data=data, *args, **kwargs)

class ApplicationTimes(AnalysisModule):
    def __init__(self):
        self._name = 'ApplicationTimes'
        AnalysisModule.__init__(self)
        
    def analyze(self, train_data, test_data, models):
        self.data = train_data
        self.data['level'] = "Coloc: " + self.data.coloc.map(coloc_map) + ", Nice: " + self.data.nice.map(str)
        print self.data.level
        return self

    def plot(self, prefix, suffix):
        keys = ['application', 'level']
        plots = []
#        for (app, level), group in self.data.groupby(keys):
        #grid = sns.FacetGrid(self.data, row='application')
        #grid.map(wrapper, x='time', hue='level', jitter=True)
        plt.figure()
        for app, data in self.data.groupby('application'):
            sns.stripplot(data=data, hue='level', x='time')
            data.time = data.time / np.min(data.time)
        plt.savefig('%s_app_times.%s' % (prefix, suffix))
        plt.figure()
        sns.stripplot(data=self.data, hue='level', x='time')
        plt.savefig('%s_app_times_normalized.%s' % (prefix, suffix))
        return self

