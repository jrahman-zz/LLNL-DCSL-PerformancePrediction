#!/bin/bash

usage() {
    echo "Usage: run.sh MEMCACHED_DIR DATA_DIR OPERATION_COUNT"
}

if [ $# -ne 3 ]; then
    usage
    exit 1
fi

MEMCACHED_DIR=${1}
DATA_DIR=${2}
OPERATIONS=${3}

BASE_DIR=$(dirname $0)/

echo "Run: Starting now..."
DATA_LOCATION="${DATA_DIR}/memcached_data/twitter_dataset_scaled"
${MEMCACHED_DIR}/memcached_client/loader -a "${DATA_LOCATION}" -s "${BASE_DIR}/servers.txt" -g 0.7 -T 1 -e 
if [ $? -ne 0 ]; then
    echo "Error: Failed to launch the run"
    exit 1
fi
echo "Run: Completed"

exit 0
