#!/bin/bash

APPS_DIR=/p/lscratche/${USER}/apps
YCSB_DIR=$APPS_DIR/ycsb-0.7.0-SNAPSHOT

WORKLOAD=$1

echo "**** Loading Memcached with YCSB **** with workload = ${WORKLOAD}"
/usr/apps/python2.7.10/bin/python ${YCSB_DIR}/bin/ycsb load memcached -s -P "${YCSB_DIR}/workloads/${WORKLOAD}" -p recordcount=500000 -p operationcount=3000000 -p "memcached.hosts=127.0.0.1" > /dev/null 2> /dev/null
