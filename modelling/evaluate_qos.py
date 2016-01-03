import util

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import seaborn as sns

metrics = ['UPDATE.99thPercentileLatency(us)', 'READ.99thPercentileLatency(us)']

"""
    Evaluate model performance against QoS metrics
"""

def dist_plot(data, metric, label, filename):
    sns.distplot(data, kde=True, rug=False, label=label, axlabel='100 * (prediction - %(metric)s/%(metric)s' % locals())
    plt.legend()
    plt.savefig(filename)
    plt.close('all')

def load_predictions(filename):
    """
    Load predictions with format:
        sample_config app_names rep observed predicted naive_sum
    """
    configs = dict()
    with open(filename, 'r') as f:
        f.readline() # Skipheader
        for line in f:
            values = line.strip().split()
            sample_config = values[0]
            app_names = values[1]
            rep = int(values[2])
            observed = float(values[3])
            predicted = float(values[4])
            naive_sum = float(values[5])
            if sample_config not in configs:
                configs[sample_config] = dict()
            if app_names not in configs[sample_config]:
                configs[sample_config][app_names] = {
                    'model': []
                }
            configs[sample_config][app_names]['observed'] = observed
            configs[sample_config][app_names]['naive_sum'] = naive_sum
            configs[sample_config][app_names]['model'].append(predicted)
    return configs

def extract_base_value(row, curves):
    """
    Extract the base qos metric values
    """
    qos_app = row['qos_app']
    metric = row['metric']
    metric_func, base_value = curves[qos_app][metric]
    return base_value

def naive_pred(row, curves, predictions):
    """
    Make a prediction of the metric based on the naive_sum
    """
    apps = row['apps']
    qos_app = row['qos_app']
    metric = row['metric']
    metric_func, base_value = curves[qos_app][metric]
    prediction = predictions[apps]
    return metric_func(prediction['naive_sum'])

def observed_pred(row, curves, predictions):
    """
    Make a prediction of the metric based on the observed value
    """
    apps = row['apps']
    qos_app = row['qos_app']
    metric = row['metric']
    metric_func, base_value = curves[qos_app][metric]
    prediction = predictions[apps]
    return metric_func(prediction['observed'])

def model_pred(row, curves, predictions):
    """
    Make a prediction of the metric based on the model prediction
    """
    apps = row['apps']
    qos_app = row['qos_app']
    metric = row['metric']
    metric_func, base_value = curves[qos_app][metric]
    predictions = predictions[apps]
    return np.mean([metric_func(value) for value in predictions['model']])

def data_available(row, curves, predictions):
    apps = row['apps']
    qos_app = row['qos_app']
    metric = row['metric']
    if apps not in predictions:
        return 0
    if qos_app not in curves:
        return 0
    if metric not in curves[qos_app]:
        return 0
    return 1

def evaluate_qos():
    configs = load_predictions('predictions')
    curves = util.load_sensitivity_curves('sensitivity_curves')
    raw_data = util.load_metrics('metric_data')

    
    metric = 'UPDATE.99thPercentileLatency(us)'
    threshold = 10 # 10% qos threshold
    for config in configs:
        predictions = configs[config]
        count = len(raw_data)
        raw_data['available'] = raw_data.apply(lambda x: data_available(x, curves, predictions), axis=1)
        data = pd.DataFrame(raw_data[raw_data['available'] == 1])
        print 'Lost %d of %d rows without predictions' % (count - len(data), count)
        data['base_value'] = data.apply(lambda x: extract_base_value(x, curves), axis=1)
        data['observed_pred'] = data.apply(lambda x: observed_pred( x, curves, predictions), axis=1)
        data['naive_pred'] = data.apply(lambda x: naive_pred(x, curves, predictions), axis=1)
        data['model_pred'] = data.apply(lambda x: model_pred(x, curves, predictions), axis=1)

        # Determine degradation vs. baseline
        data['value_degradation'] = 100 * data['value']/data['base_value']
        data['violation'] = np.zeros(len(data))
        data[np.abs(data['value_degradation'] - 100) > threshold]['violation'] = 1

        data['naive_error'] = 100 * (data['naive_pred'] - data['value']) / data['value']
        data['observed_error'] = 100 * (data['observed_pred'] - data['value']) / data['value']
        data['model_error'] = 100 * (data['model_pred'] - data['value']) / data['value']

        filtered = data[data['metric'] == metric]
        print '**** With config %s ****' % (config)
        qos_violations = np.sum(data['violation'])
        print 'With config: %s there were %d qos_violations' % (config, qos_violations)
        filename = 'plots/' + '_'.join(['ObservedError', metric, config]) + '.png'
        dist_plot(filtered['observed_error'], metric, 'Observed Error', filename)
        filename = 'plots/' + '_'.join(['NaiveError', metric, config]) + '.png'
        dist_plot(filtered['naive_error'], metric, 'Naive Error', filename)
        filename = 'plots/' + '_'.join(['ModelError', metric, config]) + '.png'
        dist_plot(filtered['model_error'], metric, 'Model Error', filename)

if __name__ == '__main__':
    evaluate_qos()
