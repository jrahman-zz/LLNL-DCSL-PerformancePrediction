#!/bin/bash

#
# INPUT: suite bmark rep cores
#

#
# OUTPUT: time mean_ipc estimated_bubble_mean median_ipc estimated_bubble_median
#

#
# NOTE: The taskset calls must be updated to reflect the appropriate processor topology
#
REPORTER_CORE=7

function run_parsec() {
	BMARK=$1
	CORES=$2
	taskset -c 0-`expr ${CORES} - 1` parsecmgmt -a run -i native -n "${CORES}" -p "${BMARK}" &> "${EXPERIMENT_LOG}"
}

function run_spec() {
	BMARK=$1
	taskset -c 0 runspec --nobuild --config research_config --action onlyrun --size ref "${BMARK}" &> "${EXPERIMENT_LOG}"
}

if [ $# -ne 4 ]; then
	echo "Error: Invalid number of arguments"
	echo "run_experiment.sh suite bmark rep cores"
	exit 1
fi

SUITE=$1
shift
BMARK=$1
shift
REP=$1
shift
CORES=$1
shift

EXPERIMENT_NAME="${SUITE}.${BMARK}.${REP}"
PID_FILE="logs/${EXPERIMENT_NAME}.pid"
OUTPUT_NAME="data/${EXPERIMENT_NAME}.reporter.perf_counters"
EXPERIMENT_LOG="logs/${EXPERIMENT_NAME}.log"

# Launch the reporter in the background
# Skip the first 15 seconds of performance counter data since that is unpacking inputs, etc
# Intervals of 1 seconds for the outputs
#
../bin/time 2> "${OUTPUT_NAME}" | 3>>"${OUTPUT_NAME}" taskset -c ${REPORTER_CORE} perf stat -I 1000 -D 15000 -e cycles,instructions --append --log-fd=3 -x ' ' ../bin/reporter 1> "${PID_FILE}" &
if [ $? -ne 0 ]; then
    echo "Error: Failed to start perf and reporter"
    exit 1
fi

# Run the batch application
if [ "x${SUITE}" == "xparsec" ]; then
	run_parsec "${BMARK}" "${CORES}"
	if [ $? -ne 0 ]; then
		echo "Error: Failed to run benchmark"
        kill `cat "${PID_FILE}"`
        rm "${PID_FILE}"
       	exit 2
	fi
elif [ "x${SUITE}" == "xspec_int" -o "x${SUITE}" == "xspec_fp" ]; then
	run_spec "${BMARK}"
	if [ $? -ne 0 ]; then
		echo "Error: Failed to run benchmark"
        kill `cat "${PID_FILE}"`
        rm "${PID_FILE}"
		exit 2
	fi
fi
# Terminate the reporter as needed
kill `cat "${PID_FILE}"`
rm "${PID_FILE}"

# Perform processing out the output data
../processing/process_perf.py "data/${EXPERIMENT_NAME}.reporter" "${OUTPUT_NAME}" &>> "${EXPERIMENT_LOG}"
if [ $? -ne 0 ]; then
	echo "Error: Failed to process timeseries"
	exit 3
fi

# Compute both the mean and median of the timeseries IPC
# values to determine the different values have
MEAN_IPC=`../processing/average_timeseries.py "data/${EXPERIMENT_NAME}.reporter.ipc" "mean" 2>> "${EXPERIMENT_LOG}"`
if [ $? -ne 0 ]; then
	echo "Error: Failed to average timeseries"
	exit 4
fi

MEDIAN_IPC=`../processing/average_timeseries.py "data/${EXPERIMENT_NAME}.reporter.ipc" "median" 2>> "${EXPERIMENT_LOG}"`
if [ $? -ne 0 ]; then
    echo "Error: Failed to average timeseries"
    exit 5
fi

REPORTER_CURVE="data/reporter_curve.bubble_size.ipc.medians"
BUBBLE_MEAN=`../processing/estimate_bubble.py ${REPORTER_CURVE} ${MEAN_IPC} 2>> "${EXPERIMENT_LOG}"`
if [ $? -ne 0 ]; then
	echo "Error: Failed to estimate bubble size"
	exit 6
fi
BUBBLE_MEDIAN=`../processing/estimate_bubble.py ${REPORTER_CURVE} ${MEDIAN_IPC} 2>> "${EXPERIMENT_LOG}"`
if [ $? -ne 0 ]; then
	echo "Error: Failed to estimate bubble size"
	exit 7
fi

# Output final result over stdout
echo "0 ${MEAN_IPC} ${BUBBLE_MEAN} ${MEDIAN_IPC} ${BUBBLE_MEDIAN}"

exit 0
