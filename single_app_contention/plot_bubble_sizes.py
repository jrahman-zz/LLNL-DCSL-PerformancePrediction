#!/bin/env python

import pandas as pd

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import seaborn as sns

def read_data():
    data = {
        'value': [],
        'bubble_type': [],
        'suite': [],
        'bmark': [],
        'name': [],
        'rep': []
        }
    with open('raw_data', 'r') as f:
        for line in f:
            values = line.strip().split()
            suite = values[0]
            bmark = values[1]
            name = '%(suite)s %(bmark)s' % locals()
            rep = int(values[2])
            mean = float(values[6])
            median = float(values[8])
            p95 = float(values[10])
            p99 = float(values[12])

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
    for suite in ['spec_fp', 'spec_int', 'parsec']:
        sns.barplot(data=data[data['suite'] == suite], x='name', y='value', hue='bubble_type')
        plt.title('Bubble Sizes')
        plt.xlabel('Batch Workload')
        plt.ylabel('Bubble Size')
        plt.legend(loc=1)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('bubble_sizes_%(suite)s.png' % locals())
        plt.close('all')

if __name__ == '__main__':
    main()
