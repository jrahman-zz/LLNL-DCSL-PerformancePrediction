#!/bin/bash

APPS_DIR=/p/lscratche/${USER}/apps
YCSB_DIR=$APPS_DIR/ycsb-0.4.0

WORKLOAD=$1
OUTPUT_PATH=$2
ABS_OUTPUT_PATH=`echo "$(cd "$(dirname "${OUTPUT_PATH}")"; pwd)/$(basename "${OUTPUT_PATH}")"`

# Filter irrelevant output we don't care about
PATTERN="\[OVERALL\]|\[CLEANUP\]|\[READ\]|\[UPDATE\]"
echo "**** Running Redis with YCSB **** with workload = ${WORKLOAD}"
/usr/apps/python2.7.10/bin/python ${YCSB_DIR}/bin/ycsb run redis -s -target 40500 -threads 2 -P "${YCSB_DIR}/workloads/${WORKLOAD}" -p recordcount=300000 -p operationcount=15000000 -p "redis.host=127.0.0.1" -p "redis.port=6379" 2>&1 | egrep "${PATTERN}" > ${ABS_OUTPUT_PATH}
