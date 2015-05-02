import util
import sklearn.base
from sklearn.pipeline import Pipeline

from sklearn import ensemble
from sklearn import linear_model
from sklearn import dummy
from sklearn import svm

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

    def fit(self, X, y):
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
        self._grid_params = [dict(ridge__alpha=util.frange(0, 20, 0.1))]
        self._name = 'Ridge'
        Model.__init__(self)
        
class GBMModel(Model):
    def __init__(self):
        self._regressor = ensemble.GradientBoostingRegressor()
        self._regressor_name = 'gbm'
        self._grid_params = [dict(
                                gbm__learning_rate=util.frange(0.05, 1, 0.05),
                                gbm__n_estimators=range(20, 300, 20),
                                gbm__max_depth=range(2, 7)
                            )]
        self._name = 'Gradient Boosted Model'
        Model.__init__(self)

class SVMLinearModel(Model):
    def __init__(self):
        self._regressor = svm.SVR(kernel='linear')
        self._regressor_name = 'svm_linear'
        self._grid_params = [dict(
                                svm_linear__C=[10**i for i in range(-5, 6)]
                            )]
        self._name = 'SVM Linear Kernel'
        Model.__init__(self)

class SVMPolynomialModel(Model):
    def __init__(self):
        self._regressor = svm.SVR(kernel='poly')
        self._regressor_name = 'svm_polynomial'
        self._grid_params = [dict(
                                svm_polynomial__C=[10**i for i in range(-5, 6)],
                                svn_polynomial__degree=range(1, 4)
                            )]
        self._name = 'SVM Polynomial Kernel'
        Model.__init__(self)

class MeanModel(Model):
    def __init__(self):
        self._regressor = dummy.DummyRegressor()
        self._regressor_name = 'mean'
        self._name = 'Naive Mean'
        Model.__init__(self)
