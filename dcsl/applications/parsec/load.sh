#!/bin/bash


usage() {
    echo "Usage: load.sh PARSEC_DIR DATA_DIR INSTANCE BMARK_NAME"
}

if [ $# -ne 4 ]; then
    usage
    exit 1
fi

BASE_DIR=$(dirname $0)/

# Path
PARSEC_DIR=${1}
if [ ! -d "${PARSEC_DIR}" ]; then
    echo "Error: PARSEC directory doesn't exist"
    usage
    exit 2
fi

if [ ! -x "${PARSEC_DIR}/bin/parsecmgmt" ]; then
    echo "Error: PARSEC directory is incorrect, can't find binary"
    usage
    exit 3
fi

# Path to directory to store data directory
DATA_DIR=${2}
if [ ! -d "${DATA_DIR}" ]; then
    echo "Error: Data parent directory doesn't exist"
    usage
    exit 4
fi

INSTANCE=${3}
BMARK_NAME=${4}

# Delete old datadir
DATA="${DATA_DIR}/parsec_data_${BMARK_NAME}"
if [ -d "${DATA}" ]; then
    echo "Load: Deleting old data directory at ${DATA} ..."
    rm -rf "${DATA}"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to delete ${DATA}"
        exit 5
    fi
    echo "Load: Deleted old data directory"
fi

# Create new, empty data directory on target drive
echo "Load: Creating new data directory at ${DATA} ..."
mkdir -p "${DATA}"
if [ $? -ne 0 ]; then
    echo "Error: Failed to create data directory"
    exit 6
fi
echo "Load: Created data directory"

echo "Load: Building benchmark"
"${PARSEC_DIR}/bin/parsecmgmt" -a build -p ${BMARK_NAME}
if [ $? -ne 0 ]; then
    echo "Error: Failed to compile benchmark"
    exit 7
fi

exit 0
