#!/bin/bash


usage() {
    echo "Usage: load.sh SPEC_DIR DATA_DIR BMARK_NAME SIZE"
}

if [ $# -ne 4 ]; then
    usage
    exit 1
fi

BASE_DIR=$(dirname $0)/

# Path
SPEC_DIR=${1}
if [ ! -d "${SPEC_DIR}" ]; then
    echo "Error: SPEC directory doesn't exist"
    usage
    exit 2
fi

if [ ! -x "${SPEC_DIR}/bin/runspec" ]; then
    echo "Error: SPEC directory is incorrect, can't find binary"
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

BMARK_NAME=${3}

SIZE=${4}
if [ "${SIZE}" != "train" -a "${SIZE}" != "test" -a "${SIZE}" != "ref" ]; then
    echo "Error: Bad size"
    usage
    exit 5
fi

# Delete old datadir
DATA="${DATA_DIR}/spec_data_${BMARK_NAME}"
if [ -d "${DATA}" ]; then
    echo "Load: Deleting old data directory at ${DATA} ..."
    rm -rf "${DATA}"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to delete ${DATA}"
        exit 6
    fi
    echo "Load: Deleted old data directory"
fi

# Create new, empty data directory on target drive
echo "Load: Creating new data directory at ${DATA} ..."
mkdir -p "${DATA}"
if [ $? -ne 0 ]; then
    echo "Error: Failed to create data directory"
    exit 7
fi
echo "Load: Created data directory"


echo "Load: Building benchmark"
(
    cd "${SPEC_DIR}"
    source shrc
    ./bin/runspec -c custom-linux64.cfg --tune base --noreportable --size ${SIZE} --action setup ${BMARK_NAME}
)
if [ $? -ne 0 ]; then
    echo "Error: Failed to compile benchmark"
    exit 8
fi

exit 0
