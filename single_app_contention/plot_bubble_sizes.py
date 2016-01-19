#!/bin/env python

import pandas as pd

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import seaborn as sns

import util

def read_data():
    
    apps = util.read_manifest()
    selected_apps = []
    for item in apps:
        suite = item['suite']
        bmark = item['bmark']
        selected_apps.append('%(suite)s %(bmark)s' % locals())
    selected_apps = set(selected_apps)

    data = {
        'value': [],
        'bubble_type': [],
        'suite': [],
        'bmark': [],
        'name': [],
        'selected': [],
        }
    with open('processed_data', 'r') as f:
        for line in f:
            values = line.strip().split()
            suite = values[-3]
            bmark = values[-2]
            name = '%(suite)s %(bmark)s' % locals()
            if name in selected_apps:
                selected = 1
            else:
                selected = 0
            mean = float(values[0])
            median = float(values[1])
            p95 = float(values[2])
            p99 = float(values[3])

            l = locals()
            for t in ['mean', 'median', 'p95', 'p99']:
                for key in data:
                    if key is 'value':
                        data['bubble_type'].append(t)
                        data['value'].append(l[t])
                    elif key is not 'bubble_type':
                        data[key].append(l[key])

    return pd.DataFrame(data)

def main():
    data = read_data()
    font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 26}
    matplotlib.rc('font', **font)
    sns.set_palette(sns.cubehelix_palette(start=2.9, n_colors=4, rot=-2, light=0.65, dark=0.35, reverse=True))

    data=data.sort('name')
    for suite in ['spec_fp', 'spec_int', 'parsec']:
        sns.barplot(data=data[data['suite'] == suite], x='name', y='value', hue='bubble_type')
        plt.title('Bubble Sizes', fontsize=18)
        plt.xlabel('Batch Workload', fontsize=18)
        plt.ylabel('Bubble Size', fontsize=18)
        plt.legend(loc=1, fontsize=18)
        plt.xticks(rotation=45)
        ax = plt.gca()
        ax.get_yaxis().get_major_formatter().set_scientific(False)
        plt.tight_layout()
        plt.savefig('plots/bubble_sizes_%(suite)s.png' % locals())
        plt.close('all')
    sns.barplot(data=data[data['selected'] == 1], x='name', y='value', hue='bubble_type')
    plt.title('Bubble Sizes', fontsize=18)
    plt.xlabel('Batch Workload', fontsize=18)
    plt.ylabel('Contention Metric', fontsize=18)
    plt.legend(loc=1, fontsize=18)
    plt.xticks(rotation=45)
    ax = plt.gca()
    ax.get_yaxis().get_major_formatter().set_scientific(False)
    plt.gcf().set_size_inches(plt.figaspect(0.4))
    plt.tight_layout()
    plt.savefig('plots/bubble_sizes.png', bbox_inches='tight')
    plt.close('all')

if __name__ == '__main__':
    main()
