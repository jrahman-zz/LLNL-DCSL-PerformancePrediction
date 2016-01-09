#!/bin/bash

#
# Given file containing raw completed experiement data, process and plot it
#

cat experiment_list.* > experiment_list
./process_experiments.sh experiment_list > raw_data
if [ $? -ne 0 ]; then
    echo "Error: Failed to process experiments"
    exit 1
fi

./process_raw_data.py raw_data | sort -rn > processed_data
if [ $? -ne 0 ]; then
    echo "Error: Failed to process raw data"
    exit 2
fi

./plot_bubble_sizes
if [ $? -ne 0 ]; then
    echo "Error: Failed to plot bubble sizes"
    exit 3
fi
