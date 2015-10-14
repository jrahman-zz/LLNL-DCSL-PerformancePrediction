#!/bin/env python

import numpy as np
import sys

#
# Purpose: Take raw experiment data and perform aggregation over multiple repitions
#

def read_data(filename):
    output = dict()
    with open(filename, 'r') as f:
        for line in f:
            values = line.strip().split()
            bmark = values[0] + "-" + values[1]
            bmark = bmark.replace('_', '-')
            if bmark not in output:
                output[bmark] = []
            values = (float(values[6]) / 1024.0, float(values[8]) / 1024.0)
            output[bmark].append(values)
    return output
                

def output(data):
    for bmark in data.keys():
        mean = np.mean(data[bmark][0])
        median = np.mean(data[bmark][1])
        sd = np.std(data[bmark])
        upper = mean + sd
        lower = mean - sd
        print("%(mean)f %(median)f %(upper)f %(lower)f %(bmark)s" % locals())

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Error: Too few arguments")
        sys.exit(1)
    output(read_data(sys.argv[1]))
