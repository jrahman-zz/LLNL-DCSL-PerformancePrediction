import util
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def analyze(train_data, test_data, models):
    keys = ['application', 'interference', 'coloc', 'nice']
    error = dict(application=[], interference=[], model=[], model_nice_name=[], coloc=[], nice=[], pred_rmse=[], base_rmse=[])
    for (app, thread, coloc, nice), group in test_data.groupby(keys):
        base_rmse = 0
        y = group['time']
        X = util.get_predictors(group).values
        mean = np.mean(y)
        base_rmse = util.rmse_error(y, mean)
        for model_name in models[app]:
            if model_name == 'mean':
                continue
            model = models[app][model_name]    
            pred = model.predict(X)
            pred_rmse = util.rmse_error(y, pred)            

            error['model_nice_name'].append(str(model))
            error['model'].append(model_name)
            error['pred_rmse'].append(pred_rmse)
            error['base_rmse'].append(base_rmse)
            error['application'].append(app)
            error['interference'].append(thread)
            error['coloc'].append(coloc)
            error['nice'].append(nice)

    error = pd.DataFrame(error)

    grid = sns.FacetGrid(error, col='model', hue='application')
    grid.map(plt.scatter, 'base_rmse', 'pred_rmse')
    grid.add_legend()

    grid = sns.FacetGrid(error, hue='model')
    grid.map(plt.scatter, 'base_rmse', 'pred_rmse')
    grid.add_legend()

    grid = sns.FacetGrid(error, hue='coloc')
    grid.map(plt.scatter, 'base_rmse', 'pred_rmse')
    grid.add_legend()
