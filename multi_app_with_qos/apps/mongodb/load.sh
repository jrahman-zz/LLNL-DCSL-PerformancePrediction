#!/bin/bash

APPS_DIR=/p/lscratche/${USER}/apps
YCSB_DIR=$APPS_DIR/ycsb-0.3.1

WORKLOAD=$1

echo "**** Loading MongoDB with YCSB **** with workload = ${WORKLOAD}"
/usr/apps/python2.7.10/bin/python ${YCSB_DIR}/bin/ycsb load mongodb -s -P "${YCSB_DIR}/workloads/${WORKLOAD}"
