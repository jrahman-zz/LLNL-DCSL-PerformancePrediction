
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
    
    def pca_analysis(self, train_data, test_data, models):
        y = train_data['time']
        X = train_data
        for drop in util.drops():
            if drop in X:
                del X[drop]
        del X['time']

        explained_variance = list()

        pca = PCA(n_components=len(X.columns))
        scaler = StandardScaler(with_std=False)
        steps = [('scaler', scaler), ('pca', pca)]
        pipeline = Pipeline(steps=steps)
        pipeline.fit(X)
        X_r = pipeline.transform(X)

        fig = plt.figure()
        plt.xlabel('Number of dimensions')
        plt.ylabel('Ratio of explained variance')
        plt.plot(range(0, len(X.columns)), pca.explained_variance_ratio_)
