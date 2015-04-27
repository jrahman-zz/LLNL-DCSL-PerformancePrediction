import util

from model import LinearModel, RidgeModel, GBMModel
from analysis_module import AnalysisModule
from sklearn import metrics

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#
# Look at the number of reps within a as it influences accuracy
#

def update(d, app, model, reps, pred, actual):
    d['application'].append(app)
    d['model'].append(model)
    d['reps'].append(reps)
    d['pred'].append(pred)
    d['actual'].append(actual)
    return d

def errors(array, data, indexes):
    diffs = pd.DataFrame(data)
    for (model, reps), group in diffs.groupby(['model', 'reps']):
        index = indexes[model]
        error = metrics.mean_squared_error(data['actual'], data['pred'])
        array[index, reps-1] = error
    return array


class LearningCurves(AnalysisModule):
    def __init__(self):
        self._name = 'LearningCurves'
        AnalysisModule.__init__(self)
    
    def analyze(self, train_data, test_data, models):

        nreps = range(1, 4)
        keys = ['application']

        error_test = dict(application=[], model=[], pred=[], actual=[], reps=[])
        error_train = dict(application=[], model=[], pred=[], actual=[], reps=[])

        models = [LinearModel, RidgeModel, GBMModel]
        model_names = [str(models[i]()) for i in range(0, len(models))]
        indexes = range(0, len(models))
        model_idx = {str(model()): idx for (model, idx) in zip(models, indexes)}
        
        test_error = np.zeros((len(models), len(nreps)))
        train_error = np.zeros((len(models), len(nreps)))

        for reps in nreps:
            for app, group in train_data.groupby(keys):
                data = group[group['rep'] <= reps]
                X = util.get_predictors(data)
                y = data['time']
                test = test_data[test_data['application'] == app]
                X_test = util.get_predictors(test)
                y_test =  test['time']
                for model in models:
                    model = model()
                    model.fit(X, y)
                    # Find predictions over the test set
                    pred = model.predict(X_test)
                    for i in range(0, len(pred)):
                       error_test = update(error_test, app, str(model), reps, pred[i], y_test.values[i])
                    # Find predictions over the training set
                    pred = model.predict(X)
                    for i in range(0, len(pred)):
                        error_train = update(error_train, app, str(model), reps, pred[i], y.values[i])
        
        test_error = errors(test_error, error_test, model_idx)
        train_error = errors(train_error, error_train, model_idx)

        for i in range(0, len(models)):
            model_name = model_names[i]
            print test_error[i, :]
            print train_error[i, :]
            plt.plot(nreps, test_error[i, :], nreps, train_error[i, :])
            plt.ylabel('Mean Squared Error')
            plt.xlabel('Runs within config')
            plt.title('Learning Curve')
           
