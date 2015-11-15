#!/bin/bash

APPS_DIR=/p/lscratche/${USER}/apps
YCSB_DIR=$APPS_DIR/YCSB

WORKLOAD=$1
OUTPUT_PATH=$2

echo "**** Running MongoDB with YCSB **** with workload = ${WORKLOAD}"
${YCSB_DIR}/bin/ycsb run mongodb -s -P ${WORKLOAD} 2>&1 > ${OUTPUT_PATH}
