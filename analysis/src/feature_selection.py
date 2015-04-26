import util

from analysis_module import AnalysisModule

from sklearn import feature_selection, cross_validation
from sklearn import ensemble
from sklearn import linear_model
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

def build_pipeline(regressor, grid_params):
    stages = {}
    stages['selector'] =feature_selection.SelectPercentile()
    stages['scaler'] = StandardScaler(with_std=False)
    stages['regressor'] = regressor
    steps = [(key, val) for key, val in stages]
    return Pipeline(steps=steps)

class FeatureSelection(AnalysisModule):
    def __init__(self):
        self._name = 'FeatureSelection'
        AnalysisModule.__init__(self)
    
    def analyze(self, train_data, test_data, models):
        models = [{'model': linear_model.LinearRegression(),
                   'grid': None}, 
                  {'model': linear_model.Ridge(),
                   'grid': [{'regressor__alpha': util.frange(0, 10, 0.2)}]},
                  {'model': ensemble.GradientBoostingRegressor(),
                   'grid': [{'regressor__learning_rate': util.frange(0.05, 0.4, 0.05),
                             'regressor__n_estimators': range(25, 300, 25),
                             'regressor__max_depth': range(2, 6)
                            }]
                  }
                ]

        for key, value in models:
            grouped = train_data.groupby('application')
            for application, group in grouped:
                features = util.get_predictors(train_data)
                y = train_data['time']`


