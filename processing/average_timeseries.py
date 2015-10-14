#!/bin/env python

import numpy as np
import sys

def read_timeseries(filename):
	timeseries = dict()
	with open(filename, 'r') as f:
		for line in f:
			values = line.strip().split()
			timeseries[float(values[0])] = float(values[1])
	return timeseries

def average_timeseries(timeseries, type):
    if type == 'median':
        return np.median(list(timeseries.values()))
    else:
        return np.mean(list(timeseries.values()))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Error: Incorrect argument count")
        print("average_timeseries.py timeseries_file")
        sys.exit(1)
    if len(sys.argv) >= 3:
        type = sys.argv[2].lower()
    else:
        type = 'mean'
    print(average_timeseries(read_timeseries(sys.argv[1]), type))
