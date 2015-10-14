
from sklearn.base import BaseEstimator

class MultiApplicationError(BaseEstimator):
    """ Predict relative error for a single model across a range of applications """
    def __init__(self, estimator):
        self._estimator = estimator
        # Per application estimator
        self._estimators = {}

    def fit(X, y):
        for application

    def predict(X):
        pass

    def
