import util

from analysis_module import AnalysisModule

import seaborn as sns
import pandas as pd
import numpy as np

class PredictionError(AnalysisModule):
    def __init__(self):
        self._name = 'PredictionError'
        AnalysisModule.__init__(self)
        
    def analyze(self, train_data, test_data, models):
        errors = dict(application=[], error=[], model=[], model_nice_name=[])
        grouped = test_data.groupby('application')
        for app, group in grouped:
            for model_name in models[app]:
                if model_name == 'mean':
                    continue
                model = models[app][model_name]

                # Only want the predictors, drop everything else 
                y = group['time']
                X = util.get_predictors(group).values
                pred = model.predict(X)
                
                # Parse and combine data
                res = abs(util.relative_error(y, pred))
                for err in res.values:
                    errors['error'].append(err)
                    errors['application'].append(app)
                    errors['model_nice_name'].append(str(model))
                    errors['model'].append(model._regressor_name)
        errors = pd.DataFrame(errors)
        plot = sns.factorplot('model', 'error', 'application', data=errors, estimator=np.mean, kind='bar', ci=95)
        plot.set_titles('Prediction Error')
        plot.set_xlabels('Relative Error (%)')
        plot.set_ylabels('Frequency')
