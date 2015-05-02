import util
import math

from model import LinearModel, RidgeModel, GBMModel
from analysis_module import AnalysisModule
from sklearn import metrics
from sklearn.cross_validation import ShuffleSplit

import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#
# Look at the number of reps within a as it influences accuracy
#

class TrainingSetSize(AnalysisModule):
    def __init__(self):
        self._name = 'TrainingSetSize'
        AnalysisModule.__init__(self)
        self.models = [LinearModel, RidgeModel, GBMModel]
    
    def analyze(self, train_data, test_data, models):
        
        self.raw_errors = dict(application=[], model=[], error=[], samples=[], error_type=[])

        # Reduce the training set to a single run per configuration
        train_data = train_data[train_data['rep'] == 1]
        test_data = test_data[test_data['rep'] == 1]
        for app, group in train_data.groupby('application'):
            test = test_data[test_data['application'] == app]
            for fraction in util.frange(0.1, 1, 0.1):
                max_samples = len(group)
                shuffler = ShuffleSplit(len(group), 100, train_size=fraction, random_state=0)
                for train_index, test_index in shuffler:
                    # Grab the slice of rows based on our shuffle and split
                    data = group.irow(train_index)
                    res = self.use_models(data, test)
                    for model_name in res:
                        for err_type in res[model_name]:
                            for error in res[model_name][err_type]:
                                self.raw_errors['application'].append(app)
                                self.raw_errors['model'].append(model_name)
                                self.raw_errors['samples'].append(len(data) * fraction)
                                self.raw_errors['error'].append(error)
                                self.raw_errors['error_type'].append(err_type)
        self.errors = pd.DataFrame(self.raw_errors)
        return self

    def use_models(self, train_data, test_data):
        y_train = train_data['time']
        X_train = util.get_predictors(train_data)
        y_test = test_data['time']
        X_test = util.get_predictors(test_data)
        errors = {}
        for model in self.models:
            model = model()
            model.fit(X_train, y_train)
            errors[str(model)] = {}
            errors[str(model)]['test'] = abs(util.relative_error(y_test, model.predict(X_test)))
            errors[str(model)]['train'] = abs(util.relative_error(y_train, model.predict(X_train)))
        return errors


    def plot(self, prefix, suffix):
        colors = {'train': 'r', 'test': 'g'}
        label = {'train': 'Training accuarcy', 'test': 'Test accuracy'}
        
        data = self.errors[self.errors['error_type'] == 'test']
        sns.factorplot('samples', 'error', data=data, hue='model', kind='point', ci=95, height=5)

        plt.savefig('%s_train_set_size.%s' % (prefix, suffix))

        for app, group in self.errors.groupby('application'):
            plt.figure()
            samples = np.unique(group['samples'])
            values = {
                    'test': {'mean': [], 'std': [], 'size': []},
                    'train': {'mean': [], 'std': [], 'size': []}
                    }

            for error_type in values.keys():
                data = group[group['error_type'] == error_type]    
                for size, d in data.groupby('samples'):
                    error = d['error']
                    values[error_type]['mean'].append(np.mean(error))
                    values[error_type]['std'].append(np.std(error))
                    values[error_type]['size'].append(size)
            processed = {}
            for error_type in values.keys():
                processed[error_type] = {}
                for metric_name, metrics in values[error_type].items():
                    processed[error_type][metric_name] = np.array(metrics)
            for error_type, value in processed.items():
                color = colors[error_type]
                sizes = values[error_type]['size']
                plt.fill_between(sizes,
                                value['mean'] - value['std'],
                                value['mean'] + value['std'],
                                alpha=0.1,
                                color=color)
            plt.plot(sizes, value['mean'], 'o-', color=color, label=labels[error_type])
            plt.savefig('%s_%s_learning_curve.%s' % (prefix, app.lower(), suffix), bbox_inches='tight')

