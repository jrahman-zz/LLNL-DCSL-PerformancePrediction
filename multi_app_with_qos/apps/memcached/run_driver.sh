#!/bin/bash

APPS_DIR=/p/lscratche/${USER}/apps
YCSB_DIR=$APPS_DIR/YCSB_with_memcache/YCSB

WORKLOAD=$1
OUTPUT_PATH=$2

# Filter irrelevant output we don't care about
PATTERN="\[OVERALL\]|\[CLEANUP\]|\[READ\]|\[UPDATE\]"

echo "**** Running Memcached with YCSB **** with workload = ${WORKLOAD}"

/usr/apps/python2.7.10/bin/python ${YCSB_DIR}/bin/ycsb run memcached -s -threads 8 -P "${YCSB_DIR}/workloads/${WORKLOAD}" -p recordcount=500000 -p operationcount=5000000 -p "memcached.hosts=127.0.0.1" 2>/dev/null 1>/dev/null | egrep "${PATTERN}" > ${OUTPUT_PATH}

