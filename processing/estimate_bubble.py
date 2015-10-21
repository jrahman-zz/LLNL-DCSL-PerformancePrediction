#!/bin/env python

import sys
from scipy import optimize
import fit_curve
import utils

#
# Purpose: From the tuned reporter curve and the measured reporter IPC estimate the
#           effective bubble size of the application(s) co-running with the reporter
#
# Parameters:
#   reporter_file - Path to file with bubble_size normalized_ipc value pairs
#   ipc - Value indicating observed reporter IPC value
#

def estimate_bubble(filename, ipc):
    (sizes, ipcs) = utils.read_bubble_size(filename)
    curve = fit_curve.fit_curve(sizes, ipcs)
    target_function = lambda x: curve(x) - ipc
    return optimize.bisect(target_function, min(sizes), max(sizes))
 
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Error: Invalid parameters")
        print("Usage: estimate_bubble.py reporter_curve ipc")
        sys.exit(1)
    print(estimate_bubble(sys.argv[1], float(sys.argv[2])))
