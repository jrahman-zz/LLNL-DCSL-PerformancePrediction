import util

from model import LinearModel, RidgeModel, GBMModel, SVMLinearModel, SVMPolynomialModel
from analysis_module import AnalysisModule
from sklearn import metrics

import seaborn as sns
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
        self.models = [LinearModel, RidgeModel, GBMModel, SVMLinearModel]
        self.model_names = [str(self.models[i]()) for i in range(0, len(self.models))]
        self.model_colors = {str(model()): model()._color for model in self.models}
        self.nreps = range(1, 11)
    
    def analyze(self, train_data, test_data, models):

        keys = ['application']
        errors = dict(application=[], model=[], error=[], reps=[], error_type=[])

        indexes = range(0, len(self.models))
        model_idx = {str(model()): idx for (model, idx) in zip(self.models, indexes)}
        
        self.test_error = np.zeros((len(self.models), len(self.nreps)))
        self.train_error = np.zeros((len(self.models), len(self.nreps)))

        for reps in self.nreps:
            for app, group in train_data.groupby(keys):
                app_data = group[group['rep'] <= reps]
                test = test_data[test_data.application == app]

                data = {'train': (util.get_predictors(app_data), app_data['time']),
                        'test': (util.get_predictors(test), test['time'])}
                for model in self.models:
                    model = model()
                    model.fit(data['train'][0], data['train'][1])
                    # Find predictions over the test set
                    for t, (X, y) in data.items():
                        pred = model.predict(X)
                        error = abs(util.relative_error(y, pred))
                        for err in error.values:
                            errors['application'].append(app)
                            errors['model'].append(str(model))
                            errors['error'].append(err)
                            errors['reps'].append(reps)
                            errors['error_type'].append(t)
        self.errors = pd.DataFrame(errors)
        return self


    def plot(self, prefix, suffix):

        colors = {'train': 'r', 'test': 'g'}
        labels = {'train': 'Training accuracy', 'test': 'Test accuracy'}
        data = self.errors[self.errors.error_type == 'test']

        sns.factorplot('reps', 'error', data=data, hue='model',
                       palette=self.model_colors, kind='point', ci=95, height=5)

        plt.savefig('%s_learning_curve.%s' % (prefix, suffix))

        for model, group in self.errors.groupby('model'):
            plt.figure()
            reps = np.unique(group.reps)
            values = {
                    'test': {'mean': [], 'std': [], 'reps': []},
                    'train': {'mean': [], 'std': [], 'reps': []}
                    }
            for error_type in values.keys():
                data = group[group.error_type == error_type]
                for reps, d in data.groupby('reps'):
                    error = d.error
                    values[error_type]['mean'].append(np.mean(error))
                    values[error_type]['std'].append(np.std(error))
                    values[error_type]['reps'].append(reps)
            processed = {}
            for error_type in values.keys():
                processed[error_type] = {}
                for metric_name, metrics in values[error_type].items():
                    processed[error_type][metric_name] = np.array(metrics)
            plots = {}
            for error_type, values in processed.items():
                color = colors[error_type]
                reps = values['reps']
                plt.fill_between(reps,
                                values['mean'] - values['std'],
                                values['mean'] + values['std'],
                                alpha=0.1,
                                color=color)
                plots[error_type] = plt.plot(reps, values['mean'], 'o-', color=color, label=labels[error_type])
            plt.legend()
            plt.savefig('%s_%s_learning_curve.%s' % (prefix, model.lower(), suffix))
        return self
           
