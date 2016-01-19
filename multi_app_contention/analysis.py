#!/usr/apps/python3.4.2/bin/python3

import numpy as np
import pandas as pd
import util
import seaborn as sns
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, FormatStrFormatter

bubble_type = 'p95_bubble'

def read_data():
    bubble_file = '../single_app_contention/processed_data'
    mean, median, p95, p99 = util.read_single_app_bubbles(bubble_file)
    multi_app_data = util.read_data('processed_experiments')
    return mean, median, p95, p99, multi_app_data

def summary(prefix, data):
    print('%s mean: %f' % (prefix, data.mean()))
    print('%s standard deviation: %f' % (prefix, data.std()))
    print('%s median: %f' % (prefix, data.median()))
    print('%s max: %f' % (prefix, data.max()))
    print('%s min: %f' % (prefix, data.min()))

def count_summary(data):
    apps_group = data.groupby('apps')
    print('Total Entries: %d' % len(data))
    print('Total Unique Combinations: %d' % len(set(data['apps'])))
    count = apps_group.size()
    for i in [1, 2, 3, 4, 5]:
        print('Total combinations with %d reps: %d' % (i, len(count[count == i])))

def plot(data, label, filename):
    sns.distplot(data*100, kde=False, rug=False, label=label, axlabel='prediction error (%)')
    plt.legend(fontsize=18)
    plt.savefig(filename, bbox_inches='tight')
    plt.close('all')

def plot_difference(data):

    counts = [2, 3, 4]
    d = {count: data[data['app_count'] == count] for count in counts}
    for count in counts:
        f = d[count][d[count]['error'] < 2.00]
        sns.distplot(100 * f['error'], kde=True, rug=False, label='%(count)d Workloads' % locals(), axlabel='prediction error (%)')
    plt.legend(fontsize=18)
    plt.xlabel('prediction error (%)', fontsize=18)
    plt.ylabel('fraction of combinations', fontsize=18)
    plt.tight_layout()
    plt.savefig('plots/overprediction.png', bbox_inches='tight')
    plt.close('all')

    #means = [np.mean(100 * data[count]['error']) for count in counts]
    d = pd.DataFrame(data)
    d['relative_error'] = 100 * d['error']
    d.sort('app_count')
    sns.pointplot(data=data, x='app_count', y='relative_error')
    plt.xlabel('Workload Count', fontsize=18)
    plt.ylabel('mean prediction error (%)', fontsize=18)
    #plt.gca().set_major_locator(MaxNLocator(integer=True))
    plt.tight_layout()
    plt.savefig('plots/overprediction_curve.png', bbox_inches='tight')
    plt.close('all')
    
if __name__ == '__main__':

    font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 26}
    matplotlib.rc('font', **font)
    #sns.set_palette(sns.cubehelix_palette(start=2.9, n_colors=3, rot=2, light=0.65, dark=0.35))
    sns.set_palette(sns.cubehelix_palette(start=2.9, n_colors=3, rot=-2, light=0.65, dark=0.35, reverse=True))
    mean_bubbles, median_bubbles, p95_bubbles, p99_bubbles, data = read_data()
    
    print('--------With NaNs--------')
    count_summary(data)
    print('------Without NaNs-------')
    # NaN compares as false against itself
    count_summary(data[data[bubble_type] == data[bubble_type]])

    # Filter out the nans
    data = data[data[bubble_type] == data[bubble_type]]
 
    # Build new column based on the sum of individual bubble sizes
    data['sum'] = np.zeros(len(data))
    for app in util.read_manifest():
        app = app['suite'] + '_' + app['bmark']
        data['sum'] += data[app] * p95_bubbles[app]

    app_groups = data.groupby('apps')
    means = app_groups.agg({bubble_type: np.mean})
    sums = app_groups.agg({'sum': np.mean})

    groups = pd.DataFrame(means)
    groups['difference'] = sums['sum'] - means[bubble_type]
    for app in util.read_manifest():
        app = app['suite'] + '_' + app['bmark']
        groups[app] = app_groups[app].agg(max)

    groups['app_count'] = app_groups['app_count'].agg(max)
    print(groups['app_count'])

    groups['error'] = groups['difference'] / groups[bubble_type]
    groups['abs_error'] = groups['error'].abs()

    print(sums['sum'])
    print(means[bubble_type])
    print(groups['difference'])
  
    plot_difference(groups)
     
    summary('Error', groups['error'])
    plot(groups['error'], 'Prediction Error (%)', 'plots/pred_error.png') 
    summary('AbsError', groups['abs_error'])
    plot(groups['error'], 'Absolute Prediction Error (%)', 'plots/abs_pred_error.png')    

    for count in [2, 3, 4]:
        d = groups[groups['app_count'] == count]
        summary('Error%(count)dApp' % locals(), d['error'])
        title = '%(count)d Application Prediction Error (%%)' % locals()
        filename = 'plots/%(count)d_app_pred_error.png' % locals() 
        plot(d['error'], title, filename)
        summary('AbsError%(count)dApp' % locals(), d['abs_error'])
        title = '%(count)d Application Absolute Prediction Error (%%)' % locals()
        filename = 'plots/%(count)d_app_abs_pred_error.png' % locals()
        plot(d['abs_error'], title, filename)
