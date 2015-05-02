import util

from analysis_module import AnalysisModule

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

class PredictionRmse(AnalysisModule):
    def __init__(self):
        self._name = 'PredictionRmse'
        AnalysisModule.__init__(self)
        
    def analyze(self, train_data, test_data, models):
        keys = ['application', 'interference', 'coloc', 'nice']
        error = dict(application=[], interference=[], model=[], coloc=[], nice=[], pred_rmse=[], base_rmse=[])
        
        self.colors = {str(model): model._color for name, model in models.values()[0].items()}
        
        for (app, thread, coloc, nice), group in test_data.groupby(keys):
            base_rmse = 0
            y = group['time']
            X = util.get_predictors(group).values
            mean = np.mean(y)
            base_rmse = util.rmse_error(y, mean)
            for model_name in models[app]:
                if model_name == 'mean':
                    continue
                model = models[app][model_name]    
                pred = model.predict(X)
                pred_rmse = util.rmse_error(y, pred)            
                error['model'].append(str(model))
                error['pred_rmse'].append(pred_rmse)
                error['base_rmse'].append(base_rmse)
                error['application'].append(app)
                error['interference'].append(thread)
                error['coloc'].append(coloc)
                error['nice'].append(nice)
        self.error = pd.DataFrame(error)
        return self

    def plot(self, prefix, suffix):
        grid = sns.FacetGrid(self.error, col='model', hue='application')
        grid.map(plt.scatter, 'base_rmse', 'pred_rmse', s=3)
        grid.add_legend()
        grid.set_ylabels('Prediction RMSE')
        grid.set_xlabels('Runtime RMSE')
        grid.set(xlim=(0,None))
        grid.set(ylim=(0,None))
        plt.savefig('%s_rmse_by_app.%s' % (prefix, suffix), bbox_inches='tight')

        grid = sns.FacetGrid(self.error, hue='model', palette=self.colors)
        grid.map(plt.scatter, 'base_rmse', 'pred_rmse', s=3)
        grid.add_legend()
        grid.set_ylabels('Prediction RMSE')
        grid.set_xlabels('Runtime RMSE')
        grid.set(xlim=(0,None))
        grid.set(ylim=(0,None))
        plt.savefig('%s_rmse_by_model.%s' % (prefix, suffix), bbox_inches='tight')

        grid = sns.FacetGrid(self.error, hue='coloc')
        grid.map(plt.scatter, 'base_rmse', 'pred_rmse', s=3)
        grid.add_legend()
        grid.set_ylabels('Prediction RMSE')
        grid.set_xlabels('Runtime RMSE')
        grid.set(xlim=(0,None))
        grid.set(ylim=(0,None))
        plt.savefig('%s_rmse_by_coloc.%s' % (prefix, suffix), bbox_inches='tight')

