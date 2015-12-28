#!/bin/bash

APPS_DIR=/p/lscratche/${USER}/apps
YCSB_DIR=$APPS_DIR/ycsb-0.4.0

WORKLOAD=$1

echo "**** Loading Redis with YCSB **** with workload = ${WORKLOAD}"
/usr/apps/python2.7.10/bin/python ${YCSB_DIR}/bin/ycsb load redis -s -P "${YCSB_DIR}/workloads/${WORKLOAD}" -p recordcount=300000 -p operationcount=15000000 -p "redis.host=127.0.0.1" -p "redis.port=6379" > /dev/null 2> /dev/null
