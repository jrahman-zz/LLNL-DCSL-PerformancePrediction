#!/bin/bash

APPS_DIR=/p/lscratche/${USER}/apps
YCSB_DIR=$APPS_DIR/ycsb-0.7.0-SNAPSHOT

WORKLOAD=$1
OUTPUT_PATH=$2
ABS_OUTPUT_PATH=`echo "$(cd "$(dirname "${OUTPUT_PATH}")"; pwd)/$(basename "${OUTPUT_PATH}")"`

# Filter irrelevant output we don't care about
PATTERN="\[OVERALL\]|\[CLEANUP\]|\[READ\]|\[UPDATE\]"
echo "**** Running Memgached with YCSB **** with workload = ${WORKLOAD}"
/usr/apps/python2.7.10/bin/python ${YCSB_DIR}/bin/ycsb run memcached -s -target 29600 -threads 8 -P "${YCSB_DIR}/workloads/${WORKLOAD}" -p recordcount=500000 -p operationcount=3000000 -p "memcached.hosts=127.0.0.1" 2>&1 | egrep "${PATTERN}" > ${ABS_OUTPUT_PATH}
