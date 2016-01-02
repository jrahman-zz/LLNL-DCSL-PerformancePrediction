#!/bin/env ${HOME}/py27/bin/python

import numpy as np
import numpy.linalg as npla
import numpy.matlib as npmat
import pandas as pd
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import seaborn as sns

import itertools
import sys
import util

"""
Attempt at a simpler scaled linear sum model

Consider each co-location combination as an equation.
For co-location A.C.D, the equation is:
c_A * B_A + c_C * B_C + c_D * B_D = B_A.C.D

Where
    c_{X} is a correction coefficient for each application
    B_{X} is the observed bubble size for application X
    and B_{X.Y.Z} is the observed bubble size for combination X.Y.Z

We create a system of equations from the data in the following form:

App.     A  B  C  D  E  F       A  B  C  D  E  F
         ----------------       ----------------     ----        --------
       | 1  0  2  0  0  0 |   |B_A 0  0  0  0  0 |  | c_A |     | B_A.C.C |
       | 0  1  0  1  0  0 |   | 0 B_B 0  0  0  0 |  | c_B |     | B_B.D   |
       | 0  0  0  1  1  0 |   | 0  0 B_C 0  0  0 |  | c_C |     | B_D.E   |
       | 1  0  0  0  0  1 |   | 0  0  0 B_D 0  0 |  | c_D |     | B_A.F   |
       | 0  0  1  0  0  1 | * | 0  0  0  0 B_E 0 | *| c_E |     | B_C.F   |
       | 0  1  0  1  1  0 |   | 0  0  0  0  0 B_F|  | c_F |   = | B_B.D.E |
       | 1  0  0  0  0  1 |    ---------------       -----      | B_A.F   |
       | 1  1  0  0  1  0 |                                     | B_A.B.E |
       | 0  0  1  0  1  0 |                                     | B_C.E   |
       | 1  0  1  1  0  0 |                                     | B_A.C.D |
        -----------------                                        ---------

The system is non-square, so an exact solution is not possible
so in turn we attempt to find a solution with minimum error

***** Input Files *****
    - experiment_data
        Data obtained from multi_app_contention experiments
        Format: (suite bmark cores)+ rep mean_ipc mean_bubble median_ipc median_bubble
    - single_buble_sizes
        Data obtained from single_app_contention experiments
        Format: mean median mean+std mean-std readable_name suite name cores

***** Output Files *****
    - sys.argv[1]
        Prediction data for different application combinations
        Format: config app_names observed prediction naive_sum

"""

 # Meta information
bubble_type = 'mean_bubble'

def dist_plot(naive_data, pred_data, naive_label, pred_label, filename):
    sns.distplot(naive_data, kde=True, rug=False, label=naive_label, axlabel='100*(prediction - ObservedBubble)/ObservedBubble')
    sns.distplot(pred_data, kde=True, rug=False, label=pred_label, axlabel='100*(prediction - ObservedBubble)/ObservedBubble')
    plt.legend()
    plt.savefig(filename)
    plt.close('all')

def dist_plotting(config, data, apps):
    cutoff = 150
    
    def func(data, filename):
        d = pd.DataFrame(data)
        d['naive_error'] = 100 * (d['naive_sum_bubble'] - d[bubble_type]) / d[bubble_type]
        d['pred_error'] = 100 * (d['pred_bubble'] - d[bubble_type]) / d[bubble_type]
        f = d[(d['naive_error'] < cutoff) & (d['naive_error'] > -cutoff)]
        g = d[(d['pred_error'] < cutoff) & (d['pred_error'] > -cutoff)]
        dist_plot(f['naive_error'], g['pred_error'], 'Naive Error', 'Model Error', filename)

    base_filename = '.'.join(['%s:%s' % (str(s), str(fraction)) for s, fraction in config.items()])
    filename = 'plots/plot.%(base_filename)s.dist.png' % locals()
    func(data, filename)

    for size in config:
        filename = 'plots/plot.%(base_filename)s.app_count:%(size)s.dist.png' % locals()
        func(data[data['app_count'] == size], filename)
    
    for app in apps:
        filename = 'plots/plot.%(base_filename)s.app:%(app)s.dist.png' % locals()
        func(data[data[app] > 0], filename)

def curve_plot(data, metric, fraction, label, filename):
    d = data.sort(fraction)
    sns.pointplot(data=d, estimator=np.median, y=metric, x=fraction, hue='type', join=True, markers=['^', 'D', 'o'])
    plt.ylabel(label)
    plt.legend()
    plt.savefig(filename)
    plt.close('all')

def curve_plotting(configurations, data, apps, counts):
    """
    Plot learning curves based on training set size
        configurations:
        data:
        apps:
    """
    # For now, trim to only include situations with equal fractions per co-location count
    for i in range(0, len(counts) - 1):
        size_a = counts[i]
        size_b = counts[i + 1]
        data = data[data['%(size_a)d_fraction' % locals()] == data['%(size_b)d_fraction' % locals()]]       
    for metric in ['mean_error', 'median_error', 'p95_error', 'std']:
        filename = 'plots/metric:%(metric)s.learning_curve.png' % locals()
        fraction='2_fraction'
        label = metric
        curve_plot(data, metric, fraction, label, filename)

def print_evaluation(config, data, apps):
    config_prefix = ':'.join(['%(key)d=%(value)f' % locals() for key, value in config.items()])
    model_types = {'pred_bubble': 'MM', 'naive_sum_bubble': 'NS'}
    for model_type, model_prefix in model_types.items():
        error = data[model_type] - data[bubble_type]
        median_error = np.median(error)
        mean_error = np.mean(error)
        std = np.std(error)
        max_error = np.max(error)
        print('%(model_prefix)s,%(config_prefix)s,median_error,%(median_error)f' % locals()) 
        print('%(model_prefix)s,%(config_prefix)s,mean_error,%(mean_error)f' % locals())
        print('%(model_prefix)s,%(config_prefix)s,max_error,%(max_error)f' % locals())
        print('%(model_prefix)s,%(config_prefix)s,std,%(std)f' % locals())
        for size in config:
            pruned = data[data['app_count'] == size]
            error = pruned[model_type] - pruned[bubble_type]
            median_error = np.median(error)
            mean_error = np.mean(error)
            std = np.std(error)
            max_error = np.max(error)
            size_prefix = '%d=%f' % (size, config[size])
            print('%(model_prefix)s,%(size_prefix)s,median_error,%(median_error)f' % locals()) 
            print('%(model_prefix)s,%(size_prefix)s,mean_error,%(mean_error)f' % locals())
            print('%(model_prefix)s,%(size_prefix)s,max_error,%(max_error)f' % locals())
            print('%(model_prefix)s,%(size_prefix)s,std,%(std)f' % locals())
        for app in apps:
            pruned = data[data[app] > 0]
            error = pruned[model_type] - pruned[bubble_type]
            median_error = np.median(error)
            mean_error = np.mean(error)
            std = np.std(error)
            max_error = np.max(error)
            print('%(model_prefix)s,app=%(app)s,median_error,%(median_error)f' % locals()) 
            print('%(model_prefix)s,app=%(app)s,mean_error,%(mean_error)f' % locals())
            print('%(model_prefix)s,app=%(app)s,max_error,%(max_error)f' % locals())
            print('%(model_prefix)s,app=%(app)s,std,%(std)f' % locals())


def create_model(data, bubble_sizes, apps, configuration):
   
    idxs = {apps[i]: i for i in range(len(apps))}
    # Stratified sampling
    samples = dict()
    for size in configuration:
        grouped = data.groupby('apps', as_index=False).agg({bubble_type: np.mean})
        samples[size] = grouped.sample(frac=configuration[size])

    size = sum([len(sample) for sample in samples.values()])
     
    # Square matrix with bubble sizes on axis
    bubble_matrix = npmat.zeros((len(apps), len(apps)))
    for app in apps:
        idx = idxs[app]
        bubble_matrix[idx,idx] = bubble_sizes[app]

    rows = size
    columns = len(apps)

    equation_matrix = npmat.zeros((rows, columns))
    rhs = npmat.zeros((rows, 1))
    i = 0
    for size in samples:
        sample = samples[size]
        for idx, applications in sample['apps'].iteritems():
            rhs[i, 0] = sample['mean_bubble'][idx]
            for app in applications.split('.'):
                equation_matrix[i, idxs[app]] += 1
            i += 1

    final_equation_matrix = equation_matrix * bubble_matrix
    
    # Find least squares solution to over-determined system
    sol, residuals, rank, s = npla.lstsq(final_equation_matrix, rhs)
    
    diff = 100 * (final_equation_matrix * sol - rhs) / rhs
    residual_rmse = np.sqrt(diff.T * diff / columns)
    p95_error = np.percentile(np.abs(diff), 95)
    std = np.std(diff)
    mean_error = abs(np.mean(diff))
    median_error = abs(np.median(diff,axis=0)[0, 0])
    
    return sol, {
                    'train.mean_error': mean_error,
                    'train.median_error': median_error,
                    'train.p95_error': p95_error,
                    'train.std': std
                }

def evaluate(data, bubble_sizes, apps, configuration):
    """
    Evaluation the accuracy of buble size predictions
    against the observer values from the experiments
    """ 
    idxs = {apps[i]: i for i in range(len(apps))}

    sol, train_stats = create_model(data, bubble_sizes, apps, configuration)

    # Build evaluation error on entire set
    pred = np.zeros(len(data))
    naive = np.zeros(len(data))
    for app in idxs:
        pred += data[app] * sol[idxs[app], 0] * bubble_sizes[app]

    # Track stats across multiple sample sizes
    error = 100*(pred - data[bubble_type])/data[bubble_type]

    p95_error = np.percentile(np.abs(error), 95)
    mean_error = np.abs(np.mean(error))
    median_error = np.abs(np.median(error))
    std = np.std(error)

    test_stats = {
                    'test.p95_error': p95_error,
                    'test.mean_error': mean_error,
                    'test.median_error': median_error,
                    'test.std': std
                 }

    for size, fraction in configuration.items():
        test_stats['%(size)d_fraction' % locals()] = fraction

    test_stats.update(train_stats)
    return sol, pred, test_stats

def save_model(data, f, configuration, rep):
    for i in range(0, data.shape[0]):
        tmp = data.iloc[i]
        observed = tmp[bubble_type]
        predicted = tmp['pred_bubble']
        naive_sum = tmp['naive_sum_bubble']
        app_names = tmp['apps']
        config = ','.join([str(key) + ':' + str(item) for key, item in configuration.items()])
        f.write('%(config)s %(app_names)s %(rep)d %(observed)f %(predicted)f %(naive_sum)f\n' % locals())

def build_predictions(data, bubble_sizes, apps, configurations, output_filename):
    """
    Create and save predictions for a range of sampling configurtaions
    """
    # Save output for later use
    with open(output_filename, 'w') as f:
        f.write('config app_names rep observed predicted naive_sum\n')
        idxs = {apps[i]: i for i in range(len(apps))}
        reps = 10
        for configuration in configurations:
            for rep in range(1, reps+1):
                sol, pred, stats = evaluate(data, bubble_sizes, apps, configuration)
                data['pred_bubble'] = pred
                naive_sum = np.zeros(len(data))
                for app in idxs:
                    naive_sum += bubble_sizes[app] * data[app]
                data['naive_sum_bubble'] = naive_sum
                save_model(data, f, configuration, rep)

def build_error_distributions(data, bubble_sizes, apps, configurations):
    """
    Build and plot a distribution of bubble prediction error over a range of sampling configurations
    """
    idxs = {apps[i]: i for i in range(len(apps))}
    for configuration in configurations:
        sol, pred, stats = evaluate(data, bubble_sizes, apps, configuration)
        data['pred_bubble'] = pred
        naive_sum = np.zeros(len(data))
        for app in idxs:
            naive_sum += bubble_sizes[app] * data[app]
        data['naive_sum_bubble'] = naive_sum
        dist_plotting(configuration, data, apps)
        print_evaluation(configuration, data, apps)

def build_learning_curves(data, bubble_sizes, apps, configurations, counts):

    idxs = {apps[i]: i for i in range(len(apps))}
    # Dictionary to hold error data for learning curves
    error_data = {'%(count)d_fraction' % locals(): [] for count in counts}
    error_data['rep'] = []
    error_data['type'] = []
    metrics = ['mean_error', 'median_error', 'p95_error', 'std']
    for metric in metrics:
        error_data[metric] = []

    # Compute naive error stats
    naive_error = np.zeros(len(data))
    for app in idxs:
        naive_error += data[app] * bubble_sizes[app]
    naive_error = 100 * (data[bubble_type] - naive_error) / data[bubble_type]
    naive_stats = {
                    'naive_sum.mean_error': np.abs(np.mean(naive_error)),
                    'naive_sum.median_error': np.abs(np.median(naive_error)),
                    'naive_sum.p95_error': np.percentile(np.abs(naive_error), 95),
                    'naive_sum.std': np.std(naive_error)
                  }

    reps = 50
    for configuration in configurations:
        print('Building for config: ' + str(configuration))
        for rep in range(reps):
            sol, pred, stats = evaluate(data, bubble_sizes, apps, configuration)
            stats.update(naive_stats)
            for prefix in ['test', 'train', 'naive_sum']:
                error_data['type'].append(prefix)
                for metric in metrics:
                    error_data[metric].append(stats['%(prefix)s.%(metric)s' % locals()])
                error_data['rep'].append(rep)
                for count in counts:
                    key = '%(count)d_fraction' % locals()
                    error_data[key].append(stats[key])

    error_data = pd.DataFrame(error_data)
    curve_plotting(configurations, error_data, apps, counts)

def build_configurations(counts, fractions):
    # Create fraction configurations
    fracs = [fractions for i in range(len(counts))]
    products = itertools.product(*fracs)
    configurations = [{counts[i]: tup[i] for i in range(len(counts))} for tup in products]
    return configurations

def main(output_filename):
       
    # Raw Data
    bubble_sizes, none = util.read_single_app_bubbles('single_bubble_sizes')
    data = util.read_contention_data('experiment_data')

    # Get set of applications in use
    apps = []
    for app_set in data['apps']:
        apps += [app for app in app_set.split('.')]
    apps = list(set(apps))
    
    # Filter NaNs out
    count = len(data)
    data = pd.DataFrame(data[data[bubble_type] == data[bubble_type]])
    print('Filtered %d NaN rows' %(count - len(data)))

    fractions = [0.05, 0.1, 0.2]
    counts = [2, 3]
    configurations = build_configurations(counts, fractions)
    build_predictions(data, bubble_sizes, apps, configurations, output_filename)

    fractions = [0.05, 0.1, 0.2]
    counts = [2, 3]
    configurations = build_configurations(counts, fractions)
    build_error_distributions(data, bubble_sizes, apps, configurations)

    fractions = [0.01, 0.025, 0.05, 0.1, 0.2, 0.3]
    counts = [2, 3]
    configurations = build_configurations(counts, fractions)
    build_learning_curves(data, bubble_sizes, apps, configurations, counts)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Error: matrix_model.py output_filename')
        sys.exit(1)
    output_filename = sys.argv[1]
    main(output_filename)
