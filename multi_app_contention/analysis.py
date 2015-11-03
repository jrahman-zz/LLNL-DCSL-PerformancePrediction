#!/bin/env python

import numpy as np
import pandas as pd
import util

def read_data():
    bubble_file = '../single_app_contention/processed_data'
    mean_bubbles, median_bubbles = util.read_single_app_bubbles(bubble_file)
    multi_app_data = util.read_data('new_output')
    return mean_bubbles, median_bubbles, multi_app_data

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
    apps_group = data[data['parsec_fluidanimate'] == 0].groupby('apps')
    count = apps_group.size()
    for i in [1, 2, 3, 4, 5]:
        print('Total combinations (No fluidanimate) with %d reps: %d' % (i, len(count[count == i])))


if __name__ == '__main__':
    mean_bubbles, median_bubbles, data = read_data()

    print('--------With NaNs--------')
    count_summary(data)
    print('------Without NaNs-------')
    # NaN compares as false against itself
    count_summary(data[data['mean_bubble'] == data['mean_bubble']])

    # Filter out the nans
    data = data[data['mean_bubble'] == data['mean_bubble']]
    data = data[data['parsec_fluidanimate'] == 0]
 
    # Build new column based on the sum of individual bubble sizes
    data['sum'] = np.zeros(len(data))
    for app in util.read_manifest():
        app = app['suite'] + '_' + app['bmark']
        data['sum'] += data[app] * mean_bubbles[app]

    app_groups = data.groupby('apps')
    means = app_groups.agg({'mean_bubble': np.mean})
    sums = app_groups.agg({'sum': np.mean})

    groups = pd.DataFrame(means)
    groups['difference'] = means['mean_bubble'] - sums['sum']
    for app in util.read_manifest():
        app = app['suite'] + '_' + app['bmark']
        groups[app] = app_groups[app].agg(max)

    groups['app_count'] = app_groups['app_count'].agg(max)
    print(groups['app_count'])

    groups['error'] = groups['difference'] / groups['mean_bubble']
    groups['abs_error'] = groups['error'].abs()

    print(sums['sum'])
    print(means['mean_bubble'])
    print(groups['difference'])
   
    summary('Error', groups['error'])
    summary('AbsError', groups['abs_error'])
    summary('Error2App', groups[groups['app_count'] == 2]['error'])
    summary('AbsError2App', groups[groups['app_count'] == 2]['abs_error'])
    summary('Error3App', groups[groups['app_count'] == 3]['error'])
    summary('AbsErr3App', groups[groups['app_count'] == 3]['abs_error'])
