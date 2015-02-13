#!/bin/bash

usage() {
    echo "Usage: run.sh YCSB_DIR OPERATION_COUNT"
}

if [ $# -eq 2 ]; then
    YCSB_DIR=${1}
    OPERATIONS="-p \"operationcount=${2}\""
else
    usage
    exit 1
fi

BASE_DIR=$(dirname $0)/../

if [ ! -x "${YCSB_DIR}/bin/ycsb" ]; then
    echo "Error: Invalid YCSB directory"
    usage
    exit 1
fi

echo "Run: Starting now..."
${BASE_DIR}/ycsb_run.sh "${YCSB_DIR}" 'cassandra-10' ${OPERATIONS} -p "hosts=localhost"
if [ $? -ne 0 ]; then
    echo "Error: Failed to launch the run"
    exit 1
fi
echo "Run: Completed"

exit 0
