
import util
import logging
import matplotlib
import matplotlib.pyplot as plt

from analysis_module import AnalysisModule

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

class PcaAnalysis(AnalysisModule):
    def __init__(self):
        self._name = 'PcaAnalysis'
    
    def analyze(self, train_data, test_data, models):
        y = train_data['time']
        self.X = train_data
        for drop in util.drops():
            if drop in self.X:
                del self.X[drop]
        del self.X['time']

        explained_variance = list()

        self.pca = PCA(n_components=len(self.X.columns))
        scaler = StandardScaler(with_std=False)
        steps = [('scaler', scaler), ('pca', self.pca)]
        pipeline = Pipeline(steps=steps)
        pipeline.fit(self.X)
        X_r = pipeline.transform(self.X)
        return self

    def plot(self, prefix, suffix):
        fig = plt.figure()
        plt.xlabel('Number of dimensions')
        plt.ylabel('Ratio of explained variance')
        plt.plot(range(0, len(self.X.columns)), self.pca.explained_variance_ratio_)
        plt.savefig('%s_pca_data.%s' % (prefix, suffix), bbox_inches='tight')
