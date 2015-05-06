import util

from analysis_module import AnalysisModule
from model import LinearModel, RidgeModel, GBMModel, SVMLinearModel

from sklearn import ensemble
from sklearn import linear_model
from sklearn import svm
from sklearn.cross_validation import StratifiedKFold, KFold
from sklearn.grid_search import GridSearchCV
from sklearn.feature_selection import RFE
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

import logging
from multiprocessing import Pool

def heatmap(data):
    rect = data.pivot('application', 'feature', 'count')
    sns.heatmap(rect)

def build_pipeline(regressor):
    stages = {}
    stages['scaler'] = StandardScaler(with_std=False)
    stages['regressor'] = regressor
    steps = [('scaler', stages['scaler']), ('regressor', stages['regressor'])]
    return Pipeline(steps=steps)

def apply_selection(self, model, train_data, test_data, target_count):
    try:
        return self._feature_selection(model, train_data, test_data, target_count)
    except Exception as e:
        logging.exception("Exception: %s" % (str(e)))
        return None

class FeatureSelection(AnalysisModule):
    def __init__(self):
        self._name = 'FeatureSelection'
        self._models = [LinearModel, RidgeModel, GBMModel, SVMLinearModel]
        self._cost_function = util.rmse_error
        AnalysisModule.__init__(self)

    def analyze(self, train_data, test_data, models):
#        models = [{'model': linear_model.LinearRegression(),
#                   'grid': {},
#                   'name': 'Linear',
#                   'color': 'blue'}, 
#                  {'model': linear_model.Ridge(),
#                   'grid': [{'regressor__alpha': util.frange(0, 10, 0.2)}],
#                   'name': 'Ridge',
#                   'color': 'red'},
#                  {'model': ensemble.GradientBoostingRegressor(),
#                   'grid': [{'regressor__learning_rate': util.frange(0.05, 1, 0.05),
#                             'regressor__n_estimators': range(20, 300, 20),
#                             'regressor__max_depth': range(2, 7)
#                            }],
#                   'name': 'GBM',
#                   'color': 'yellow'
#                  },
##                  {'model': svm.SVR(kernel='poly'),
##                   'grid': [{
##                            'regressor__degree': range(1, 4),
##                            'regressor__C': [10**i for i in range(-5, 6)]
##                       }],
##                   'name': 'SVMPoly'
##                  },
#                  {'model': svm.SVR(kernel='linear'),
#                   'grid': [{
#                            'regressor__C': [10**i for i in range(-5, 6)]
#                       }],
#                   'name': 'SVMLinear',
#                   'color': 'green'
#                  }
#                ]
#
#        errors = dict(application=[], model=[], feature_count=[], error=[], error_type=[])
#        features = dict(application=[], model=[], feature=[], count=[]) 
#        
#        max_feature_count = len(util.get_predictors(train_data).columns)
#        for feature_count in range(4, (max_feature_count / 2) * 2, 2):
#            for app, group in train_data.groupby('application'):
#                for model_params in models:
#                    model = model_params['model']
#                    grid = model_params['grid']
#                    name = model_params['name']
#
#                    pipeline = build_pipeline(model)
#                    rfe = RFE(pipeline, feature_count, step=1)
#                    cv = GridSearchCV(rfe, grid, cv=10)
#                    test = test_data[test_data['application'] == app]
#                    
#                    X_train = util.get_predictors(group)
#                    y_train = group['time']
#                    X_test = util.get_predictors(test)
#                    y_test = test['time']
#                    
#                    cv.fit(X_train, y_train)
#                
#                    # Build feature heatmap
#                    for feature in self._extract_features(rfe, X_train):
#                        features['application'].append(app)
#                        features['model'].append(name)
#                        features['feature'].append(feature)
#                        features['count'].append(feature)
#
#                    types = {'train': (X_train, y_train), 'test': (X_test, y_test)}
#                    for err_type, (X, y) in types:
#                        pred = rfe.predict(X)
#                        for error in util.relative_error(y, pred):
#                            errors['application'].append(app)
#                            errors['model'].append(str(model))
#                            errors['feature_count'].append(feature_count)
#                            errors['error'].append(error)
#                            errors['error_type'].append('train')
#        self.errors = pd.DataFrame(errors)
#        
#        # Fetch minimum count for each feature, application, and model
#        features = pd.DataFrame(features)
#        self.features = dict(application=[], model=[], feature=[], count=[])
#        for model, model_group in features.groupby('model'):
#            for app, app_group in model_group.groupby('application'):
#                for feature, feature_group in app_group.groupby('feature'):
#                    min_count = feature_group.feature_count.min()
#                    self.features['application'].append(app)
#                    self.features['model'].append(app)
#                    self.features['feature'].append(feature)
#                    self.features['count'].append(min_count)
#        self.features = pd.DataFrame(self.features)
        feature_choices = self.feature_selection(train_data, test_data, models)

        models = {str(model()): model() for model in self._models}

        errors = dict(application=[], model=[], error=[], feature_count=[])
        for model, feature_selection in feature_choices.items():
            for feature_count, features in feature_selection:
                model = models[model]
                for app, group in train_data.groupby('application'):
                    test = test_data[test_data.application == app]
                    data = {'train': {'X': util.get_predictors(group)[features], 'y': group.time},
                            'test': {'X': util.get_predictors(test)[fetures], 'y': test.time}}
                    model.fit(data['train']['X'], data['train']['y'])
                    for err_type, d in data.items():
                        pred = model.pred(d['X'])
                        actual = d['y']
                        error = util.relative_error(actual, pred)
                        for i in range(0, len(error)):
                            errors['application'].append(app)
                            errors['model'].append(str(model))
                            errors['error'].append(error[i])
                            errors['feature_count'].append(len(features))
        self.errors = pd.DataFrame(errors)
        return self
            
    def plot(self, prefix, suffix):
        colors = {'train': 'r', 'test': 'g'}
        label = {'train': 'Training accuracy', 'test': 'Test accuracy'}
 
        data = self.errors[self.errors['error_type'] == 'test']
        sns.factorplot('feature_count', 'error', data=data, hue='model', kind='point', ci=95)

        for app, group in self.errors.groupby('application'):
            plt.figure()
            feature_count = np.unique(group['feature_count'])
            values = {
                    'test': {'mean': [], 'std': [], 'count': []},
                    'train': {'mean': [], 'std': [], 'count': []}
                    }
            for error_type in values.keys():
                data = group[group['error_type'] == error_type]
                for count, d in data.groupby('feature_count'):
                    error = d['error']
                    values[error_type]['mean'].append(np.mean(d))
                    values[error_type]['std'].append(np.std(d))
                    values[error_type]['count'].append(count)
            processed = {}
            for error_type in values.keys():
                processed[error_type] = {}
                for metric_name, matrics in values[error_type].items():
                    processed[error_type][matric_name] = np.array(metrics)
            for error_type, value in processed.items():
                color = colors[error_type]
                counts = values[error_type]['count']
                plt.fill_between(values[error_type]['count'],
                                value['mean'] - value['std'],
                                value['mean'] + value['std'],
                                alpha=0.1,
                                color=color)
                plt.plot(counts, value['mean'], 'o-', color=color, label=labels[error_type])
            plt.savefig('%s_%s_features.%s' % (prefix, app.lower(), suffix), bbox_inches='tight')

        grid = sns.FacetGrid(self.features, col='model')
        grid.map(heatmap)
        plt.savefig('%s_feature_heatmpa.%s' % (prefix, suffix), bbox_inches='tight')
        return self

    def feature_selection(self, train_data, test_data, models):
        """ Perform RFE over all features """

        target_count = 4
        selected_features = {}
        
        pool = Pool(len(self._models))
        models = [model() for model in self._models]
        operations = [
                (
                    model,
                    pool.apply_async(
                        apply_selection, (self, model, train_data, test_data, target_count)
                    )
                 )
                for model in models]
        results = [(model, operation.get()) for model, operation in operations]
        for model, features in results:
            selected_features[str(model)] = features


    def _feature_selection(self, model, train_data, test_data, target_count):
        features = util.get_predictors(train_data).columns
        selected_features = dict()
        while (len(features) > target_count):
            logging.info('Checking %d features', len(features)) # DEBUG
            
            error = dict(application=[], err_type=[], model=[], cand=[], pred=[], actual=[])
            # Remove a single feature at a time
            for i in range(0, len(features)):
                candidates = list(features)
                candidates.pop(i)
#               logging.info('Candidates: %s', str(candidates))
                inserted = 0 # DEBUG


                # Build the models based on the data
                for app, data in train_data.groupby('application'):
                    test = test_data[test_data.application == app]
                    samples = {'train': { 'X': util.get_predictors(data)[candidates], 'y': data.time},
                            'test': {'X': util.get_predictors(test)[candidates], 'y': test.time}}
                    model.fit(samples['train']['X'], samples['train']['y'])
                     
                    pred = model.predict(samples['test']['X'])
                    actual = samples['test']['y']
    #               logging.info('Adding %d for candidate %d with type %s', len(actual), i, stype)
                    for j in range(0, len(pred)):
                        error['application'].append(app)
                        error['model'].append(str(model))
                        error['err_type'].append('test')
                        error['pred'].append(pred[j])
                        error['actual'].append(actual[j:j])
                        error['cand'].append(i)
                        inserted = inserted + 1 # DEBUG
                logging.info('Inserted %d for candidate %d', inserted, i)

            # Now post process to find the actual best candiate for removal
            data = pd.DataFrame(error)
            errs = data[data.err_type == 'test']
            candidate_errors = []
            for candidate in range(0, len(features)):
                logging.info('Checking candidate %d', candidate)
                d = errs[errs.cand == candidate]
                if len(d.actual) == 0:
                    logging.error('Candidate %d for model %s has no values', candidate, str(model))
                    continue
                logging.info('In _feature_selection: len(d.actual) = %d, len(d.pred) = %d', len(d.actual), len(d.pred))
                candidate_error = self._cost_function(d.actual.values, d.pred.values)
                candidate_errors.append(candidate_error)

            print "Errors: %s" % (str(candidate_errors))
            candidate = np.argmax(candidate_errors)
            args = (features[candidate], candidate_errors[candidate])
            print "Selected candidate %s with error %d" % args
            features.pop(candidate)
        
            selected_features[len(features)] = features
        return selected_features


    def _extract_features(self, rfe, X):
        support = rfe.support_
        indexes = [i for i in range(0, len(support)) if support[i]]
        return [str(s) for s in X.keys()[indexes]]
