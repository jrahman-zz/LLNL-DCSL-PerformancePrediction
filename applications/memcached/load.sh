#!/bin/bash


usage() {
    echo "Usage: load.sh MEMCACHED_DIR DATA_DIR PID_FILE MEMORY"
}

if [ $# -ne 4 ]; then
    usage
    exit 1
fi

BASE_DIR=$(dirname $0)/

# Path
MEMCACHED_DIR=${1}
if [ ! -d "${MEMCACHED_DIR}" ]; then
    echo "Error: Memcached directory doesn't exist"
    usage
    exit 1
fi

if [ ! -x "${MEMCACHED_DIR}/memcached_client/loader" -o ! -r "${MEMCACHED_DIR}/twitter_dataset/twitter_dataset_unscaled" ]; then
    echo "Error: Memcached data directory is incorrect"
    usage
    exit 1
fi

if [ ! -x "${MEMCACHED_DIR}/bin/memcached" ]; then
    echo "Error: Cannot find memcached binary"
    usage
    exit 1
fi

# Path to directory to store data directory
DATA_DIR=${2}
if [ ! -d "${DATA_DIR}" ]; then
    echo "Error: Data parent directory doesn't exist"
    usage
    exit 1
fi

PID_FILE=${3}

MEMORY=${4}

SCALE_FACTOR=`expr ${MEMORY} / 300`
if [ $? -ne 0 ]; then
    echo "Error: Failed to calculate the scaling factor"
    usage
    exit 1
fi

# Delete old datadir
if [ -d "${DATA_DIR}/memcached_data" ]; then
    echo "Load: Deleting old data directory at ${DATA_DIR}/memcached_data..."
    rm -rf "${DATA_DIR}/memcached_data"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to delete ${DATA_DIR}/memcached_data"
        exit 1
    fi
    echo "Load: Deleted old data directory"
fi

# Create new, empty data directory on target drive
echo "Load: Creating new data directory at ${DATA_DIR}/memcached_data..."
mkdir -p "${DATA_DIR}/memcached_data"
if [ $? -ne 0 ]; then
    echo "Error: Failed to create data directory"
    exit 1
fi
echo "Load: Created data directory"

echo "Load: Starting server..."
${MEMCACHED_DIR}/bin/memcached -d -P "${PID_FILE}" -m "${MEMORY}" -t 4
if [ $? -ne 0 ]; then
    echo "Error: Failed to start memcached"
    exit 1
fi

OUTPUT_FILE="${DATA_DIR}/memcached_data/"
DATASET_FILE="${MEMCACHED_DIR}/twitter_dataset/twitter_dataset_unscaled"

# Load the data as needed
echo "Load: building scaled dataset"
echo "${MEMCACHED_DIR}/memcached_client/loader -a \"${DATASET_FILE}\" -s \"${BASE_DIR}/servers.txt\" -S ${SCALE_FACTOR} -o \"${OUTPUT_FILE}\""
${MEMCACHED_DIR}/memcached_client/loader -a "${DATASET_FILE}" -s "${BASE_DIR}/servers.txt" -S ${SCALE_FACTOR} -o "${OUTPUT_FILE}"
if [ $? -ne 0 ]; then
    echo "Error: Failed to load data into Memcached"
    exit 1
fi

echo "Load: Stopping memcached..."
kill `cat ${PID_FILE}`
if [ $? -ne 0 ]; then
    echo "Error: Failed to stop memcached"
    exit 2
fi
rm "${PID_FILE}"

exit 0
