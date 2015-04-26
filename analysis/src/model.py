import util
import sklearn.base
from sklearn.pipeline import Pipeline

from sklearn import ensemble
from sklearn import linear_model
from sklearn import dummy

from sklearn.preprocessing import StandardScaler
from sklearn.grid_search import GridSearchCV

class Model:
    def __init__(self):
        self._grid_params = None
        self._grid = None
        self._model = None
        self._pipeline = Pipeline([
                    ('scaling', StandardScaler()),
                    (self._regressor_name, self._regressor)
                ])

    def fit(self, y, X):
        if self._grid_params is None:
            self._model = self._pipeline.fit(X, y)
        else:
            grid = GridSearchCV(self._pipeline,
                                param_grid=self._grid_params,
                                cv=10,
                                n_jobs=-1)
            self._model = grid.fit(X, y), 

    def predict(self, X):
        return self._model.predict(X)

    def __str__(self):
        return self._name

class LinearModel(Model):
    def __init__(self):
        self._regressor = linear_model.LinearRegression()
        self._regressor_name = 'lm'
        self._name = 'Linear Model'
        Model.__init__(self)

class RidgeModel(Model):
    def __init__(self):
        self._regressor = linear_model.Ridge()
        self._regressor_name = 'ridge'
        self._grid_params = [dict(ridge__alpha=util.frange(0, 10, 0.2))]
        self._name = 'Ridge'
        Model.__init__(self)
        
class GBMModel(Model):
    def __init__(self):
        self._regressor = ensemble.GradientBoostingRegressor()
        self._regressor_name = 'gbm'
        self._grid_params = [dict(
                                gbm__learning_rate=util.frange(0.05, 0.4, 0.05),
                                gbm__n_estimators=range(25, 300, 25),
                                gbm__max_depth=range(2, 6)
                            )]
        self._name = 'Gradient Boosted Model'
        Model.__init__(self)

class MeanModel(Model):
    def __init__(self):
        self._regressor = dummy.DummyRegressor()
        self._regressor_name = 'mean'
        self._name = 'Naive Mean'
        Model.__init__(self)
