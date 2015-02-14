#!/bin/bash

usage() {
    echo "Usage: run.sh MONGODB_DIR DATA_DIR YCSB_DIR OPERATION_COUNT"
}

if [ $# -eq 4 ]; then
    # Ignore lower arguments, they are dummy arguments for the sake of the interface
    YCSB_DIR=${3}
    OPERATIONS="-p \"operationcount=${4}\""
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

PARAMS="${OPERATIONS}"

echo "Run: Starting now..."
${BASE_DIR}/ycsb_run.sh "${YCSB_DIR}" 'mongodb' ${PARAMS}
if [ $? -ne 0 ]; then
    echo "Error: Failed to launch the run"
    exit 1
fi
echo "Run: Completed"

exit 0
