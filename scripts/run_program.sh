#!/bin/bash

# Directly run a standalone program via the perf tool to collect performance counter data

DELAY=$1
shift
EXPERIMENT=$1
shift

PERF_COUNTER_FILE="${EXPERIMENT}.perf_counters"

./bin/time 2> "${PERF_COUNTER_FILE}" && perf stat -I 250 -e cycles,instructions -x ' ' -D ${DELAY} "$@" |& tee -a "${EXPERIMENT}.perf_counters"
