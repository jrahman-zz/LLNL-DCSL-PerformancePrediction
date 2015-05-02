import util

from model import LinearModel, RidgeModel, GBMModel, SVMLinearModel, SVMPolynomialModel
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
        self.models = [LinearModel, RidgeModel, GBMModel]
        self.model_names = [str(self.models[i]()) for i in range(0, len(self.models))]
        self.nreps = range(1, 4)
    
    def analyze(self, train_data, test_data, models):

        keys = ['application']

        error_test = dict(application=[], model=[], pred=[], actual=[], reps=[])
        error_train = dict(application=[], model=[], pred=[], actual=[], reps=[])

        indexes = range(0, len(self.models))
        model_idx = {str(model()): idx for (model, idx) in zip(self.models, indexes)}
        
        self.test_error = np.zeros((len(self.models), len(self.nreps)))
        self.train_error = np.zeros((len(self.models), len(self.nreps)))

        for reps in self.nreps:
            for app, group in train_data.groupby(keys):
                data = group[group['rep'] <= reps]
                X = util.get_predictors(data)
                y = data['time']
                test = test_data[test_data['application'] == app]
                X_test = util.get_predictors(test)
                y_test =  test['time']
                for model in self.models:
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
        
        self.test_error = errors(self.test_error, error_test, model_idx)
        self.train_error = errors(self.train_error, error_train, model_idx)

    def plot(self, prefix, suffix):
        for i in range(0, len(self.models)):
            model_name = self.model_names[i]
            plt.figure()
            plt.plot(self.nreps, self.test_error[i, :], self.nreps, self.train_error[i, :], '-')
            plt.ylabel('Mean Squared Error')
            plt.xlabel('Runs within config')
            plt.title('Learning Curve')
            plt.savefig('%s_%s_learning_curve.%s' % (prefix, model_name, suffix))
           
