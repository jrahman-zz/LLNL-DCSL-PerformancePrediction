#!/bin/bash

usage() {
    echo "Usage: cleanup.sh SPEC_DIR DATA_DIR BMARK_NAME"
}

if [ $# -ne 3 ]; then
    echo "Error: Invalid arguments"
    usage
    exit 1
fi

SPEC_DIR=${1}

# Remove temp dir
DATA_DIR="${2}/spec_data_${3}"
if [ -d "${DATA_DIR}" ]; then
    echo "Cleanup: Removing ${DATA_DIR}..."
    rm -rf "${DATA_DIR}"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to cleanup data"
        exit 2
    fi
    echo "Cleanup: Removed ${DATA_DIR}"
fi

# Remove run files

RUN_DIR="${SPEC_DIR}/benchspec/CPU2006/${3}/"
echo "Cleanup: Checking for ${RUN_DIR}/run/"
if [ -d "${RUN_DIR}/run/" ]; then
    echo "Cleanup: Removing ${RUN_DIR}/run/"
    rm -rf "${RUN_DIR}"/run/*
    if [ $? -ne 0 ]; then
        echo "Error: Failed to cleanup run directory"
        exit 3
    fi
else
    echo "Error: No run directory found"
    exit 4
fi

exit 0
