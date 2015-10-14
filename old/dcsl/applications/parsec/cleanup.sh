#!/bin/bash

usage() {
    echo "Usage: cleanup.sh PARSEC_DIR DATA_DIR INSTANCE BMARK_NAME"
}

if [ $# -ne 4 ]; then
    echo "Error: Invalid arguments"
    usage
    exit 1
fi

PARSEC_DIR=${1}
INSTANCE=${3}
BMARK_NAME=${4}

# Remove temp dir
DATA_DIR="${2}/parsec_data_${BMARK_NAME}"
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
if [ -x "${PARSEC_DIR}/bin/parsecmgmt" ]; then 
    "${PARSEC_DIR}/bin/parsecmgmt" -a clean -p "${BMARK_NAME}"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to clean parsec"
        exit 3
    fi
else
    echo "Error: PARSEC_DIR invalid"
    exit 4
fi

exit 0
