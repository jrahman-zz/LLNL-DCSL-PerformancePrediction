#!/bin/bash

APPS_DIR=/p/lscratche/${USER}/apps
YCSB_DIR=$APPS_DIR/YCSB_with_memcache/YCSB

WORKLOAD=$1
OUTPUT_PATH=$2
ABS_OUTPUT_PATH=`cd "${OUTPUT_PATH}"; pwd`

# Filter irrelevant output we don't care about
PATTERN="\[OVERALL\]|\[CLEANUP\]|\[READ\]|\[UPDATE\]"
cd "${YCSB_DIR}"
echo "**** Running Memcached with YCSB **** with workload = ${WORKLOAD}"
/usr/apps/python2.7.10/bin/python ${YCSB_DIR}/bin/ycsb run memcached -s -threads 8 -P "${YCSB_DIR}/workloads/${WORKLOAD}" -p recordcount=500000 -p operationcount=5000000 -p "memcached.hosts=127.0.0.1" | egrep "${PATTERN}" > ${ABS_OUTPUT_PATH}
