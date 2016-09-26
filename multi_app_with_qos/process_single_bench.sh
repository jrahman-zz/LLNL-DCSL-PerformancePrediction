#!/bin/bash

#
# Given file containing raw completed experiement data, process and plot it
#

#cat experiment_list.* > experiment_list
#srun -n1 -N1 -c16 -ppdebug sh -c "cat experiment_list | xargs -n1 -d'\n' -P4 process_experiments_single_bench.sh" > raw_data
srun -n1 -N1 -c16 -ppdebug sh -c "cat experiment_list_mongodb_1_app_1_core_15_rep | xargs -n1 -d'\n' -P4 process_experiments_single_bench.sh" > raw_data
if [ $? -ne 0 ]; then
    echo "Error: Failed to process experiments"
    exit 1
fi

./process_raw_data_single_bench.py raw_data | sort -rn > processed_data_single_bench_mongodb
if [ $? -ne 0 ]; then
    echo "Error: Failed to process raw data"
    exit 2
fi

#./plot_bubble_sizes.py
#if [ $? -ne 0 ]; then
#    echo "Error: Failed to plot bubble sizes"
#    exit 3
#fi
