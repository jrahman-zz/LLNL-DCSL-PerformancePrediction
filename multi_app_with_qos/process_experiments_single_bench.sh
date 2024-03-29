#!/bin/bash

#
# Given an experiment manifest, process all output from reporters
#

SUITE=`echo "${1}" | cut -d ' ' -f 1`
BENCHMARK=`echo "${1}" | cut -d ' ' -f 2`
CORES=`echo "${1}" | cut -d ' ' -f 3`
QOS_NAME=`echo "${1}" | cut -d ' ' -f 4`
WORKLOAD_NAME=`echo "${1}" | cut -d ' ' -f 5`
OUTPUTDATA=`echo "${1}" | cut -d ' ' -f 6`
REP=`echo "${1}" | cut -d ' ' -f 7`

#EXPERIMENT_NAME="${SUITE}.${BENCHMARK}.${REP}.reporter"
EXPERIMENT_NAME="${QOS_NAME}.${CORES}.${SUITE}.${BENCHMARK}.${REP}"

#FILE="data/${EXPERIMENT_NAME}.perf_counters"
FILE="${OUTPUTDATA}.perf"
if [ ! -r "${FILE}" ]; then
    echo "Error: Cannot find ${FILE}" 1>&2
    exit 1
fi

echo "Processing ${FILE}..." 1>&2

../processing/process_perf.py "single_batch_data/${QOS_NAME}/${EXPERIMENT_NAME}" "${FILE}"
if [ $? -ne 0 ]; then
    echo "Error: Failed to process ${FILE}" 1>&2
    exit 2
fi

#REPORTER_CURVE="../data/reporter_curve.bubble_size.ipc"
#REPORTER_CURVE="../data/${QOS_NAME}_curve.bubble_size.ipc"
REPORTER_CURVE="${QOS_NAME}_curve.bubble_size.ipc"
PYTHON="${HOME}/py271/bin/python"

MEAN_IPC=`../processing/average_timeseries.py "single_batch_data/${QOS_NAME}/${EXPERIMENT_NAME}.ipc" "mean"`
if [ $? -ne 0 ]; then
    echo "Error: Failed to average ${EXPERIMENT_NAME}.ipc - ${MEAN_IPC}" 1>&2
    MEAN_IPC='NaN'
    BUBBLE_MEAN='NaN'
else
    echo "Estimating mean bubble" 1>&2
    BUBBLE_MEAN=`${PYTHON} ../processing/estimate_bubble.py "${REPORTER_CURVE}" "${MEAN_IPC}"`
    if [ $? -ne 0 ]; then
        echo "Error: Failed to calculate mean bubble - ${BUBBLE_MEAN}" 1>&2
        BUBBLE_MEAN='NaN'
    fi
fi

MEDIAN_IPC=`../processing/average_timeseries.py "single_batch_data/${QOS_NAME}/${EXPERIMENT_NAME}.ipc" "median"`
if [ $? -ne 0 ]; then
    echo "Error: Failed to average ${EXPERIMENT_NAME}.ipc - ${MEDIAN_IPC}" 1>&2
    MEDIAN_IPC='NaN'
    BUBBLE_MEDIAN='NaN'
else
    echo "Estimating median bubble" 1>&2
    BUBBLE_MEDIAN=`${PYTHON} ../processing/estimate_bubble.py "${REPORTER_CURVE}" "${MEDIAN_IPC}"`
    if [ $? -ne 0 ]; then
        echo "Error: Failed to calculate median bubble - ${BUBBLE_MEDIAN}" 1>&2
        BUBBLE_MEDIAN='NaN'
    fi
fi

P95_IPC=`../processing/average_timeseries.py "single_batch_data/${QOS_NAME}/${EXPERIMENT_NAME}.ipc" "95th"`
if [ $? -ne 0 ]; then
    echo "Error: Failed to average ${EXPERIMENT_NAME}.ipc - ${P95_IPC}" 1>&2
    P95_IPC='NaN'
    BUBBLE_P95='NaN'
else
    BUBBLE_P95=`${PYTHON} ../processing/estimate_bubble.py "${REPORTER_CURVE}" "${P95_IPC}"`
    if [ $? -ne 0 ]; then
        echo "Error: Failed to calculate P95 bubble - ${BUBBLE_P95}" 1>&2
        BUBBLE_P95='NaN'
    fi
fi

P99_IPC=`../processing/average_timeseries.py "single_batch_data/${QOS_NAME}/${EXPERIMENT_NAME}.ipc" "99th"`
if [ $? -ne 0 ]; then
    echo "Error: Failed to average ${EXPERIMENT_NAME}.ipc - ${MEDIAN_IPC}" 1>&2
    P99_IPC='NaN'
    BUBBLE_P99='NaN'
else
 BUBBLE_P99=`${PYTHON} ../processing/estimate_bubble.py "${REPORTER_CURVE}" "${P99_IPC}"`
    if [ $? -ne 0 ]; then
        echo "Error: Failed to calculate P99 bubble - ${BUBBLE_P99}" 1>&2
        BUBBLE_P99='NaN'
    fi
fi

echo "${SUITE} ${BENCHMARK} ${REP} ${CORES} 0 ${MEAN_IPC} ${BUBBLE_MEAN} ${MEDIAN_IPC} ${BUBBLE_MEDIAN} ${P95_IPC} ${BUBBLE_P95} ${P99_IPC} ${BUBBLE_P99}"

echo "Processed ${FILE}" 1>&2
