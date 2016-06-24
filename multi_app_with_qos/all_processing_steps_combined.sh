#!/bin/bash

if [ "$1" = "" ]; then
    echo "Usage: all_processing_steps_combined.sh   <qos_app_name>"
    exit 1
fi

qos_app_name=$1
echo "QoS app is: $qos_app_name"

#Create the sensitivity curve of the QoS app
sensitivity_curve_outfile="$qos_app_name.sensitivity_curve.outfile"
./process_sensitivity.py $qos_app_name $sensitivity_curve_outfile

if [ $? -ne 0 ]; then
    echo "Error: Sensitivity Curve Creation Failed"
    exit 1
fi
echo "Succesfully created sensitivity curve"


#Calculate single app bubble sizes

#Check if the experiment_list file is the correct one

qos_name_count=`grep -c $qos_app_name experiment_list`
echo "There are $qos_name_count instances of $qos_app_name in experiment_list file."
if [ $qos_name_count -ne 19 ]; then
    echo "Error: Do not have the expected number of entries for the QoS app name in the experiment_list file"
    exit 2
fi
	
cat experiment_list | xargs -n1 -d'\n' -P4 process_experiments_single_bench.sh > "raw_data.$qos_app_name"
if [ $? -ne 0 ]; then
    echo "Error: Failed to process single batch experiments"
    exit 3
fi

./process_raw_data_single_bench.py "raw_data.$qos_app_name" | sort -rn > "processed_experiments_single_bench_wrt_$qos_app_name"
if [ $? -ne 0 ]; then
    echo "Error: Failed to process raw data for single batch experiments"
    exit 4
fi


echo "Succesfully calculated single benchmark bubble sizes"

./process_experiments.py 1 > "processed_experiments_wrt_$qos_app_name"
if [ $? -ne 0 ]; then
    echo "Error: Failed to process raw data for single batch experiments"
    exit 5
fi

echo "Succesfully calculated combined bubble sizes for muktiple benchmarks"

echo "We have generated the following files: "
echo "-------------------------------------"
echo "$qos_app_name"."_curve.bubble_size.ipc"
echo "processed_experiments_single_bench_wrt_$qos_app_name"
echo "processed_experiments_multiple_batch_wrt_$qos_app_name"
