#!/bin/bash

function help {
    echo "run_bubble EXPERIMENT_NAME [DELAY [MEASUREMENT_INTERVAL [BUBBLE_INTERVAL [SINGLE_LOOP]]]]"
}

if [ $# -lt 2 ]; then
  help
  exit 1
fi

EXPERIMENT_NAME=$1
shift

if [ $# -ge 1 ]; then
  DELAY=$1
  shift
else
  DELAY=0
fi

if [ $# -ge 1 ]; then
  MEASUREMENT_INTERVAL=$1
  shift
else
  MEASUREMENT_INTERVAL=250
fi

if [ $# -ge 1 ]; then
  BUBBLE_INTERVAL=$1
  shift
else
  BUBBLE_INTERVAL=2000
fi

if [ $# -ge 1 ]; then
  SINGLE_LOOP=$1
else
  SINGLE_LOOP=0
fi

echo "Bubble: ${BUBBLE_INTERVAL}, Measurement: ${MEASUREMENT_INTERVAL}"

BINARY_DIR=$(cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)/../bin

"${BINARY_DIR}/time" 2> "${EXPERIMENT_NAME}.bubble.perf_counters" && 3>> "${EXPERIMENT_NAME}.bubble.perf_counters" perf stat --log-fd=3 -e instructions,cycles -I ${MEASUREMENT_INTERVAL} -D ${DELAY} "${BINARY_DIR}"/bubble 1.3 "${BUBBLE_INTERVAL}" "${SINGLE_LOOP}" |& tee "${EXPERIMENT_NAME}.bubble.size"
