#!/bin/bash

APPS_DIR=/p/lscratche/${USER}/apps
YCSB_DIR=$APPS_DIR/YCSB

WORKLOAD=$1

echo "**** Loading MongoDB with YCSB **** with workload = ${WORKLOAD}"
${YCSB_DIR}/bin/ycsb load mongodb -s -P "${YCSB_DIR}/workloads/${WORKLOAD}"
