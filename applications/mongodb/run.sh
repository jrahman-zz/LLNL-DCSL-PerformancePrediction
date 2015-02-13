#!/bin/bash

usage() {
    echo "Usage: run.sh YCSB_DIR [OPERATION_COUNT]"
}

if [ $# -eq 1 ]; then
    YCSB_DIR=${1}
    OPERATIONS=""
elif [ $# -eq 2 ]; then
    YCSB_DIR=${1}
    OPERATIONS="-P \"operationcount=${2}\""
else
    usage
    exit 1
fi

if [ ! -x "$YCSB_DIR}/bin/ycsb" ]; then
    echo "Error: Invalid YCSB directory"
    usage
    exit 1
fi

PARAMS="${OPERATIONS}"

echo "Run: Starting now..."
ycsb_run.sh "${YCSB_DIR}" 'mongodb' ${PARAMS}
if [ $? -ne 0 ]; then
    echo "Error: Failed to launch the run"
    exit 1
fi
echo "Run: Completed"

exit 0
