#!/bin/bash


usage() {
    echo "Usage: start.sh MEMCACHED_DIR DATA_DIR PID_FILE MEMORY(MB) [THREADS]"
}

if [ $# -lt 4 ]; then
    usage
    exit 1
fi

# Path
MEMCACHED_DIR=${1}
if [ ! -d "${MEMCACHED_DIR}" ]; then
    echo "Error: Memcached directory doesn't exist"
    usage
    exit 1
fi

BASE_DIR=$(dirname $0)/../

if [ ! -x "${MEMCACHED_DIR}/bin/memcached" -o ! -x "${MEMCACHED_DIR}/memcached_client/loader" -o ]; then
    echo "Error: Memcached directory is incorrect"
    usage
    exit 1
fi

if [ ! -r "${MEMCACHED_DIR}/twitter_dataset/twitter_dataset_unscaled" ]; then
    echo "Error: Cannot find Twitter dataset"
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

if [ $# -gt 4 ]; then
    THREADS=${5}
else
    THREADS=4
fi

SCALE_FACTOR=`expr ${MEMORY} / 300`

echo "Start: Starting server..."
${MEMCACHED_DIR}/bin/memcached -d -P "${PID_FILE}" -m "${MEMORY}" -t "${THREADS}"
if [ $? -ne 0 ]; then
    echo "Error: Failed to start memcached"
    exit 1
fi

# Load the data as needed
echo "Start: Loading data into memcached..."
${MEMCACHED_DIR}/memcached_client/loader -a "${DATA_DIR}/memcached_data/twitter_dataset_scaled" -s "${BASE_DIR}/servers.txt"
if [ $? -ne 0 ]; then
    echo "Error: Failed to load data into Memcached"
    exit 2
fi
echo "Start: Loaded data into Memcached"

exit 0
