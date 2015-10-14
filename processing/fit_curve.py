#!/bin/env python

from scipy import interpolate
import matplotlib.pyplot as plt
import numpy as np
import sys

#
# Fit a curve to the bubble_size-ipc curve
# fit_curve.py
#

def fit_curve(x, y):
    return interpolate.interp1d(x, y, kind=1)    

def predict(curve, x):
    return curve(x)

def plot_fit(curve, x, y):
    max_x = max(x)
    min_x = min(x)
    xnew = np.arange(min_x, max_x)
    ynew = curve(xnew)
    plt.plot(x, y, 'o', xnew, ynew, '-')
    plt.show()

def read_bubble_size(filename):
    sizes = []
    ipcs = []
    with open(filename, 'r') as f:
        for line in f:
            values = line.strip().split()
            sizes.append(int(float(values[0])))
            ipcs.append(float(values[1]))
    return (sizes, ipcs)
            
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Need to give the filename')
        sys.exit(1)
    
    (sizes, ipcs) = read_bubble_size(sys.argv[1])
    curve = fit_curve(sizes, ipcs)
    plot_fit(curve, sizes, ipcs)

