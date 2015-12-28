#!/bin/bash

APPS_DIR=/p/lscratche/${USER}/apps
YCSB_DIR=$APPS_DIR/ycsb-0.4.0

WORKLOAD=$1
OUTPUT_PATH=$2

# Filter irrelevant output we don't care about
PATTERN="\[OVERALL\]|\[CLEANUP\]|\[READ\]|\[UPDATE\]"

echo "**** Running MongoDB with YCSB **** with workload = ${WORKLOAD}"
/usr/apps/python2.7.10/bin/python ${YCSB_DIR}/bin/ycsb run mongodb -s -target 22500 -threads 8 -P "${YCSB_DIR}/workloads/${WORKLOAD}" -p recordcount=500000 -p operationcount=5000000 2> /dev/null | egrep "${PATTERN}" > ${OUTPUT_PATH}
