import util

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def analyze(train_data, test_data, models):
    keys = ['application']
    error = dict(application=[], model=[], model_nice_name=[], error=[])
    grouped = test_data.groupby(keys)
    for app, group in grouped:
        y=group['time']
        X = util.get_predictors(group).values
        for model_name in models[app]:
            if model_name == 'mean':
                continue
            model = models[app][model_name]
            pred = model.predict(X)

            res = util.relative_error(y, pred)
            for err in res.values:
                error['error'].append(err)
                error['model'].append(model_name)
                error['model_nice_name'].append(str(model))
                error['application'].append(app)

    error = pd.DataFrame(error)
    grid = sns.FacetGrid(error, col='model')
    grid.map(plt.hist, 'error', bins=40)

