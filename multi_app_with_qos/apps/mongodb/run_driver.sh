#!/bin/bash

APPS_DIR=/p/lscratche/${USER}/apps
YCSB_DIR=$APPS_DIR/ycsb-0.3.1

WORKLOAD=$1
OUTPUT_PATH=$2

PATTERN="\[OVERALL\]|\[CLEANUP\]|\[READ\]|\[UPDATE\]"

echo "**** Running MongoDB with YCSB **** with workload = ${WORKLOAD}"
/usr/apps/python2.7.10/bin/python ${YCSB_DIR}/bin/ycsb run mongodb -s -threads 2 -P "${YCSB_DIR}/workloads/${WORKLOAD}" -p recordcount=100000 -p operationcount=1000000 2> /dev/null | egrep "${PATTERN}" > ${OUTPUT_PATH}
