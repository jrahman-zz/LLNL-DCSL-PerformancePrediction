#!/bin/env python

import numpy as np
import sys

#
# Purpose: Take raw experiment data and perform aggregation over multiple repitions
#

def read_data(filename):
    mean = dict()
    median = dict()
    with open(filename, 'r') as f:
        for line in f:
            values = line.strip().split()
            bmark = values[0] + "-" + values[1]
            bmark = (bmark.replace('_', '-'), values[0], values[1], values[3])
            if bmark not in mean:
                mean[bmark] = []
                median[bmark] = []
            mean[bmark].append(float(values[6]) / 1024.0)
            median[bmark].append(float(values[8]) / 1024.0)
    return mean, median
                

def output(data):
    mean, median = data
    for bmark in mean.keys():
        name = bmark[0]
        bmark_suite = bmark[1]
        bmark_name = bmark[2]
        bmark_cores = bmark[3]
        dmean = np.mean(mean[bmark])
        dmedian = np.mean(median[bmark])
        sd = np.std(mean[bmark])
        upper = dmean + sd
        lower = dmean - sd
        print("%(dmean)f %(dmedian)f %(upper)f %(lower)f %(name)s %(bmark_suite)s %(bmark_name)s %(bmark_cores)s" % locals())

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Error: Too few arguments")
        sys.exit(1)
    output(read_data(sys.argv[1]))
