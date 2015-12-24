#!/bin/bash

APPS_DIR=/p/lscratche/${USER}/apps
YCSB_DIR=$APPS_DIR/YCSB_with_memcache/YCSB

WORKLOAD=$1

cd "${YCSB_DIR}"

echo "**** Loading Memcached with YCSB **** with workload = ${WORKLOAD}"
/usr/apps/python2.7.10/bin/python ${YCSB_DIR}/bin/ycsb load memcached -s -P "${YCSB_DIR}/workloads/${WORKLOAD}" -p recordcount=500000 -p operationcount=5000000 -p "memcached.hosts=127.0.0.1" 
