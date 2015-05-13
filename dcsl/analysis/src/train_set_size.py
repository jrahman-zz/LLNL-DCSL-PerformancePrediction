import util
import math

from model import LinearModel, RidgeModel, GBMModel, SVMLinearModel
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
        self.models = [LinearModel, RidgeModel, GBMModel, SVMLinearModel]
    
    def analyze(self, train_data, test_data, models):
        
        self.raw_errors = dict(application=[], model=[], error=[], samples=[], error_type=[])

        self.colors = {str(model): model._color for name, model in models.values()[0].items()}

        # Reduce the training set to a single run per configuration
        train_data = train_data[train_data['rep'] == 1]
        test_data = test_data[test_data['rep'] == 1]
        for app, group in train_data.groupby('application'):
            test = test_data[test_data['application'] == app]
            max_samples = len(group)
            for samples in range(4, max_samples - 1, 4):
                fraction = float(samples) / float(max_samples)
                shuffler = ShuffleSplit(max_samples, 50, train_size=fraction, test_size=None, random_state=0)
                for train_index, test_index in shuffler:
                    # Grab the slice of rows based on our shuffle and split
                    data = group.irow(train_index)
                    res = self.use_models(data, test)
                    for model_name in res:
                        for err_type in res[model_name]:
                            for error in res[model_name][err_type]:
                                self.raw_errors['application'].append(app)
                                self.raw_errors['model'].append(model_name)
                                self.raw_errors['samples'].append(samples)
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
        labels = {'train': 'Training accuarcy', 'test': 'Test accuracy'}
        
        data = self.errors[self.errors['error_type'] == 'test']
        grid = sns.factorplot('samples', 'error', data=data, hue='model', kind='point',
                        estimator=np.median, palette=self.colors, ci=95, height=5)
        grid.set_xlabels('Unique Configurations')
        grid.set_ylabels('Median Relative Error (%)')

        plt.savefig('%s_train_set_size.%s' % (prefix, suffix))

        for app, group in self.errors.groupby('application'):
            for model, app_data in group.groupby('model'):
                fig = plt.figure()
                samples = np.unique(app_data['samples'])
                values = {
                        'test': {'median': [], 'std': [], 'size': []},
                        'train': {'median': [], 'std': [], 'size': []}
                        }

                for error_type in values.keys():
                    data = app_data[app_data['error_type'] == error_type]    
                    for size, d in data.groupby('samples'):
                        error = d['error']
                        values[error_type]['median'].append(np.median(error))
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
                                    value['median'] - value['std'],
                                    value['median'] + value['std'],
                                    alpha=0.1,
                                    color=color)
                    plt.plot(sizes, value['median'], 'o-', color=color, label=labels[error_type])
                plt.legend()
                plt.ylabel('Median Relative Error (%)')
                plt.xlabel('Unique Configurations')
                args = (prefix, app.lower(), model.lower(), suffix)
                plt.savefig('%s_%s_%s_training_set.%s' % args, bbox_inches='tight')
                plt.close(fig)

