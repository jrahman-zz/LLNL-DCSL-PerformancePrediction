#!/bin/bash

#
# Given an experiment manifest, process all output from reporters
#

cat "${1}" | while read LINE; do
    SUITE=`echo "${LINE}" | cut -d ' ' -f 1`
    BENCHMARK=`echo "${LINE}" | cut -d ' ' -f 2`
    REP=`echo "${LINE}" | cut -d ' ' -f 3`
    CORES=`echo "${LINE}" | cut -d ' ' -f 4`

    EXPERIMENT_NAME="${SUITE}.${BENCHMARK}.${REP}.reporter"
    FILE="data/${EXPERIMENT_NAME}.perf_counters"
    if [ ! -r "${FILE}" ]; then
        echo "Error: Cannot find ${FILE}" 1>&2
        continue
    fi

    echo "Processing ${FILE}..." 1>&2

    ../processing/process_perf.py "data/${EXPERIMENT_NAME}" "${FILE}"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to process ${FILE}" 1>&2
        continue
    fi
    
    MEAN_IPC=`../processing/average_timeseries.py "data/${EXPERIMENT_NAME}.ipc"`
    if [ $? -ne 0 ]; then
        echo "Error: Failed to average ${EXPERIMENT_NAME}.ipc - ${MEAN_IPC}" 1>&2
        continue
    fi

    MEDIAN_IPC=`../processing/average_timeseries.py "data/${EXPERIMENT_NAME}.ipc" "median"`
    if [ $? -ne 0 ]; then
        echo "Error: Failed to average ${EXPERIMENT_NAME}.ipc - ${MEDIAN_IPC}" 1>&2
        continue
    fi

    REPORTER_CURVE="data/reporter_curve.bubble_size.ipc.medians"
    echo "Estimating mean bubble" 1>&2
    BUBBLE_MEAN=`../processing/estimate_bubble.py "${REPORTER_CURVE}" "${MEAN_IPC}"`
    if [ $? -ne 0 ]; then
        echo "Error: Failed to calculate mean bubble - ${BUBBLE_MEAN}" 1>&2
        continue
    fi

    echo "Estimating median bubble" 1>&2
    BUBBLE_MEDIAN=`../processing/estimate_bubble.py "${REPORTER_CURVE}" "${MEDIAN_IPC}"`
    if [ $? -ne 0 ]; then
        echo "Error: Failed to calculate median bubble - ${BUBBLE_MEDIAN}" 1>&2
        continue
    fi

    echo "${SUITE} ${BENCHMARK} ${REP} ${CORES} 0 ${MEAN_IPC} ${BUBBLE_MEAN} ${MEDIAN_IPC} ${BUBBLE_MEDIAN}"

    echo "Processed ${FILE}" 1>&2
done
