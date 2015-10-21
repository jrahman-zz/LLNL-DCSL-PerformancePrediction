#!/bin/bash

BUBBLE_CORE=0
REPORTER_CORE=7

#
# Generates reporter curve by running the reporter and bubble side by side
#

EXPERIMENT_NAME="reporter_curve"
OUTPUT_NAME="data/${EXPERIMENT_NAME}.reporter.perf_counters"
PID_FILE="${EXPERIMENT_NAME}.pid"

BINARY_DIR=$(cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)/../bin

# Launch the reporter in the background
# Intervals of 500 milliseconds for the outputs
"${BINARY_DIR}/time" 2> "${OUTPUT_NAME}" | 3>>"${OUTPUT_NAME}" taskset -c "${REPORTER_CORE}" perf stat -I 500 -D 100 -e cycles,instructions --log-fd=3 -x ' ' "${BINARY_DIR}/reporter" 1> "${EXPERIMENT_NAME}.pid" &
if [ $? -ne 0 ]; then
    echo "Error: Failed to start perf and reporter"
    exit 1
fi

MEASUREMENT_INTERVAL=500
DELAY=100
BUBBLE_LOOPS=1
BUBBLE_INTERVAL=10000
BUBBLE_SIZE_FILE="data/${EXPERIMENT_NAME}.bubble.size"
BUBBLE_PERF_COUNTERS="data/${EXPERIMENT_NAME}.bubble.perf_counters"

# Start the bubble
# The time binary is run first to generate an absolute timestamp at the beginning
# The perf util output will contain relative offsets that will be added to the absolute
# initial timestamp and the post-processing script will perform registration between
# the reporter timestamps and the bubble timestamps
"${BINARY_DIR}/time" 2> "${BUBBLE_PERF_COUNTERS}" && 3>> "${BUBBLE_PERF_COUNTERS}" taskset -c "${BUBBLE_CORE}" perf stat --log-fd=3 -e instructions,cycles -I ${MEASUREMENT_INTERVAL} -D ${DELAY} "${BINARY_DIR}"/bubble 1.20 "${BUBBLE_INTERVAL}" "${BUBBLE_LOOPS}" |& tee "${BUBBLE_SIZE_FILE}"
if [ $? -ne 0 ]; then
	echo "Error: Failed to run bubble"
	exit 2
fi

# Terminate the reporter once the bubble finishes running
kill `cat "${PID_FILE}"`
rm "${PID_FILE}"

# Run the post-processing script on the output
../processing/process_bubble.py "data/${EXPERIMENT_NAME}" "${BUBBLE_SIZE_FILE}" "${OUTPUT_NAME}" 0.2
if [ $? -ne 0 ]; then
	echo "Error: Failed to process the bubble"
	exit 3
fi
