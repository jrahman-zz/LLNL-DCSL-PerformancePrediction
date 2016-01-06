#!/bin/env python

import numpy as np
import sys

#
# Purpose: Take raw experiment data and perform aggregation over multiple repitions
#

def read_data(filename):
    mean = dict()
    median = dict()
    p95 = dict()
    p99 = dict()
    with open(filename, 'r') as f:
        for line in f:
            values = line.strip().split()
            bmark = values[0] + "-" + values[1]
            bmark = (bmark.replace('_', '-'), values[0], values[1], values[3])
            if bmark not in mean:
                mean[bmark] = []
                median[bmark] = []
                p95[bmark] = []
                p99[bmark] = []
            mean[bmark].append(float(values[6]) / 1024.0)
            median[bmark].append(float(values[8]) / 1024.0)
            p95[bmark].append(float(values[10]) / 1024.0)
            p99[bmark].append(float(values[12]) / 1024.0)
    return mean, median, p95, p99
                

def output(data):
    mean, median, p95, p995 = data
    for bmark in mean.keys():
        name = bmark[0]
        bmark_suite = bmark[1]
        bmark_name = bmark[2]
        bmark_cores = bmark[3]
        dmean = np.mean(mean[bmark])
        dmedian = np.mean(median[bmark])
        dp95 = np.mean(p95[bmark])
        dp99 = np.mean(p99[bmark])
        meanstd = np.std(mean[bmark])
        medianstd = np.std(median[bmark])
        p95std = np.std(p95[bmark])
        p99std = np.std(p99[bmark])
        print("%(dmean)f %(dmedian)f %dp95)f %(dp99)f %(meanstd)f %(medianstd)fi %(p95std)f %(p99std)f %(name)s %(bmark_suite)s %(bmark_name)s %(bmark_cores)s" % locals())

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Error: Too few arguments")
        sys.exit(1)
    output(read_data(sys.argv[1]))
