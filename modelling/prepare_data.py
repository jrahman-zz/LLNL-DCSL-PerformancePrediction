#!/bin/env python

import sys
import numpy as np
import util

#
# Prepare data from raw multi-application runs into a format suitable for ALS
#

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print('Error: Usage prepare_data.py filepath datafile xlabelfile ylabelfile')
        sys.exit(1)

    bubble = 'mean_bubble'
    data = util.read_data(sys.argv[1])
    data = data[data[bubble] == data[bubble]]
    data = data[data['parsec_fluidanimate'] == 0]
    datafile = sys.argv[2]
    xlabelfile = sys.argv[3]
    ylabelfile = sys.argv[4]

    # Filter out NaNs
    with open(datafile, 'w') as f:
        aggregated = data.groupby('apps').agg({bubble: np.mean})
        f.write('apps bubble\n')
        for tup in aggregated.itertuples():
            f.write('%s %f\n' % (tup[0], float(tup[1])))

    xmaxlabel = 0
    ymaxlabel = 0
    ylabels = set()
    xlabels = set()
    with open(xlabelfile, 'w') as xfile:
        with open(ylabelfile, 'w') as yfile:
            for app in data['apps']:
                apps = app.split('.')
                for i in range(len(apps)):
                    first_app = apps[i]
                    remaining_apps = '.'.join(apps[0:i] + apps[i+1:])
                    if first_app not in ylabels:
                        yfile.write('%s %d\n' % (first_app, ymaxlabel))
                        ymaxlabel += 1
                        ylabels.add(first_app)
                    if remaining_apps not in xlabels:
                        xfile.write('%s %d\n' % (remaining_apps, xmaxlabel))
                        xmaxlabel += 1
                        xlabels.add(remaining_apps)
