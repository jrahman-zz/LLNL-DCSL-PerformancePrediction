#!/usr/apps/python3.4.2/bin/python3

import numpy as np
import numpy.linalg as npla
import numpy.matlib as npmat
import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt

import itertools
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

"""

 # Meta information
bubble_type = 'mean_bubble'
#sample_fractions = [0.05, 0.1, 0.15, 0.2, 0.25]
sample_fractions = [0.2]
sizes = [2, 3]

def dist_plot(naive_data, pred_data, naive_label, pred_label, filename):
    sns.distplot(naive_data, kde=False, rug=False, label=naive_label, axlabel='100*(observed_bubble - prediction)/observed_bubble')
    sns.distplot(pred_data, kde=False, rug=False, label=pred_label, axlabel='100*(observed_bubble - prediction)/observed_bubble')
    plt.legend()
    plt.savefig(filename)
    plt.close('all')

def dist_plotting(config, data, apps):
    for size in config:
        pruned = data[data['app_count'] == size]
        naive_error = 100 * (pruned[bubble_type] - pruned['naive_sum_bubble']) / pruned[bubble_type]
        pred_error = 100 * (pruned[bubble_type] - pruned['pred_bubble']) / pruned[bubble_type]

        filename = ':'.join(['%s=%s' % (str(size), str(fraction)) for size, fraction in config.items()])
        filename = 'plot_' + filename
        dist_plot(naive_error, pred_error, 'Naive Error', 'Model Error', '%(filename)s:app_count=%(size)s.dist.pdf' % locals())

    for app in apps:
        pruned = data[data[app] > 0]
        naive_error = 100 * (pruned[bubble_type] - pruned['naive_sum_bubble']) / pruned[bubble_type]
        pred_error = 100 * (pruned[bubble_type] - pruned['pred_bubble']) / pruned[bubble_type]

        filename = ':'.join(['%s=%s' % (str(size), str(fraction)) for size, fraction in config.items()])
        filename = 'plot_' + filename
        dist_plot(naive_error, pred_error, 'Naive Error', 'Model Error', '%(filename)s:app=%(app)s.dist.pdf' % locals())

def curve_plot(data, metric, fraction, label, filename):
    d = data.sort(fraction)
    sns.pointplot(data=d, estimator=np.median, y=metric, x=fraction, join=True)
    plot.ylabel(label)
    plt.legend()
    plt.savefig(filename)
    plt.close('all')

def curve_plotting(configurations, data, apps):
    """
    Plot learning curves based on training set size
        configurations:
        data:
        apps:
    """
    sizes = [size for size in configurations]
    # For now, trim to only include situations with equal fractions per co-location count
    for i in range(0, len(sizes) - 1):
        size_a = sizes[i]
        size_b = sizes[i + 1]
        data = data[data['%(size_a)d_fraction' % locals()] == data['%(size_b)d_fraction' % locals()]]       
    for metric in ['mean_error', 'median_error', 'max_error', 'std']:
        filename = 'metric:%(metric)s.learning_curve.pdf' % locals()
        fraction='2_fraction'
        label = metric
        curve_plot(data, metric, fraction, label, filename)

def evaluate(config, data, apps):
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


def main():
 
    # Create fraction configurations
    fracs = [sample_fractions for i in range(len(sizes))]
    fractions = itertools.product(*fracs)
    configurations = [{sizes[i]: tup[i] for i in range(len(sizes))} for tup in fractions]

    # Dictionary to hold error data for learning curves
    error_data = {'%(size)d_fraction' % locals(): [] for size in sizes}
    for metric in ['mean_error', 'median_error', 'max_error', 'std']:
        error_data[metric] = []
    
    # Raw Data
    bubble_sizes, none = util.read_single_app_bubbles('single_bubble_sizes')
    data = util.read_data('experiment_data')

    # Get set of applications in use
    apps = []
    for app_set in data['apps']:
        apps += [app for app in app_set.split('.')]
    apps = list(set(apps))

    idxs = {apps[i]: i for i in range(len(apps))}
 
    # Pre-NaN filter count
    count = len(data)
    
    # Filter NaNs out
    data = pd.DataFrame(data[data[bubble_type] == data[bubble_type]])
    print('Filtered %d NaN rows' %(count - len(data)))

    for configuration in configurations:
        # Stratified sampling
        samples = dict()
        for size in configuration:
            grouped = data.groupby('apps', as_index=False).agg({bubble_type: np.mean})
            sd = data.groupby('apps', as_index=False).agg({bubble_type: np.std})
            samples[size] = grouped.sample(frac=configuration[size])

        size = sum([len(sample) for sample in samples.values()])
     
        # Square matrix with bubble sizes on axis
        bubble_matrix = npmat.zeros((len(apps), len(apps)))
        for app in apps:
            idx = idxs[app]
            bubble_matrix[idx,idx] = bubble_sizes[app]

        rows = size
        columns = len(apps)

        print('Rows: %(rows)d, columns: %(columns)d' % locals())

        equation_matrix = npmat.zeros((rows, columns))
        rhs = npmat.zeros((rows, 1))
        naive_sum = npmat.zeros((rows, 1))
        i = 0
        for size in samples:
            sample = samples[size]
            for idx, applications in sample['apps'].items():
                rhs[i, 0] = sample['mean_bubble'][idx]
                for app in applications.split('.'):
                    equation_matrix[i, idxs[app]] += 1
                    naive_sum[i,0] += bubble_sizes[app]
                i += 1

        final_equation_matrix = equation_matrix * bubble_matrix
        print(str(final_equation_matrix) + ' = ' + str(rhs))
    
        sol, residuals, rank, s = npla.lstsq(final_equation_matrix, rhs)
        diff = final_equation_matrix * sol
        diff = diff - rhs
        residual_rmse = np.sqrt(diff.T * diff / columns)
        max_error = np.max(diff)
        std = np.std(diff)
        mean_error = np.mean(diff)
        print('MM,rank,%(rank)d' % locals())
        print('MM,residual_rmse,%(residual_rmse)f' % locals())
        print('MM,train_max_error,%(max_error)f' % locals())
        print('MM,train_std,%(std)f' % locals())
        print('MM,train_mean_error,%(mean_error)f' % locals())
    
        diff = naive_sum - rhs
        residual_rmse = np.sqrt(diff.T * diff / columns)
        max_error = np.max(diff)
        std = np.std(diff)
        mean_error = np.mean(diff)
        print('NS,residual_rmse,%(residual_rmse)f' % locals())
        print('NS,max_error,%(max_error)f' % locals())
        print('NS,std,%(std)f' % locals())
        print('NS,mean_error,%(mean_error)f' % locals())

        # Build evaluation error on entire set
        pred = np.zeros(len(data))
        naive = np.zeros(len(data))
        for app in idxs:
            pred += data[app] * sol[idxs[app], 0] * bubble_sizes[app]
            naive += data[app] * bubble_sizes[app]
        data['pred_bubble'] = pred
        data['naive_sum_bubble'] = naive

        # Track stats across multiple sample sizes
        error = data[bubble_type] - data['pred_bubble']

        for size, fraction in configuration.items():
            error_data['%(size)d_fraction' % locals()].append(fraction)
        error_data['mean_error'].append(np.mean(error))
        error_data['median_error'].append(np.median(error))
        error_data['max_error'].append(np.max(np.abs(error)))
        error_data['std'].append(np.std(error))

        dist_plotting(configuration, data, apps)
        evaluate(configuration, data, apps)
    
    error_data = pd.DataFrame(error_data)
    curve_plotting(configurations, error_data, apps)

if __name__ == '__main__':
    main()
