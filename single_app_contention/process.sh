#!/bin/bash

#
# Given file containing raw completed experiement data, process and plot it
#

./process_raw_data.py raw_data | sort -rn > processed_data
./plot_bubble_sizes
./plot_reporter_curve
