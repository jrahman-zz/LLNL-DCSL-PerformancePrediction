import util

import pandas as pd

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as pyplot
import seaborn as sns

metrics = ['UPDATE.99thPercentileLatency(us)', 'READ.99thPercentileLatency(us)']

"""
    Evaluate model performance against QoS metrics
"""

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
                    'predicted': []
                }
            configs[sample_config][app_names]['observed'] = observed
            configs[sample_config][app_names]['naive_sum'] = naive_sum
            configs[sample_config][app_names]['predicted'].append(predicted)
    return configs

def extract_base_value(row, curves):
    """
    Extract the base qos metric values
    """
    qos_app = row['qos_app']
    metric = row['metric']
    metric_func, percent_fun, base_value = curves[qos_app][metric]
    return base_value

def naive_pred(row, curves, predictions):
    """
    Make a prediction of the metric based on the naive_sum
    """
    apps = row['apps']
    qos_app = row['qos_app']
    metric = row['metric']
    metric_func, percent_func, base_value = curves[qos_app][metric]
    prediction = predictions[apps]
    return metric_func(prediction['naive_sum'])

def observed_pred(row, curves, predictions):
    """
    Make a prediction of the metric based on the observed value
    """
    apps = row['apps']
    qos_app = row['qos_app']
    metric = row['metric']
    metric_func, percent_func, base_value = curves[qos_app][metric]
    prediction = predictions[apps]
    return metric_func(prediction['observed'])

def pred_pred(row, curves, predictions):
    """
    Make a prediction of the metric based on the model prediction
    """
    apps = row['apps']
    qos_app = row['qos_app']
    metric = row['metric']
    metric_func, percent_func, base_value = curves[qos_app][metric]

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

    for config in configs:
        predictions = configs[config]
        count = len(raw_data)
        raw_data['available'] = raw_data.apply(lambda x: data_available(x, curves, predictions), axis=1)
        data = pd.DataFrame(raw_data[raw_data['available'] == 1])
        print 'Lost %d of %d rows without predictions' % (count - len(data), count)
        data['base_value'] = data.apply(lambda x: extract_base_value(x, curves), axis=1)
        data['observed_pred'] = data.apply(lambda x: observed_pred( x, curves, predictions), axis=1)
        data['naive_pred'] = data.apply(lambda x: naive_pred(x, curves, predictions), axis=1)


if __name__ == '__main__':
    evaluate_qos()
