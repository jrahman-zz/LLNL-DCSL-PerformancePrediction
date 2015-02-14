#!/bin/bash

usage() {
    echo "Usage: start.sh MONGODB_HOME DATA_DIR"
}

if [ $# -ne 2 ]; then
    usage
    exit 1
fi

MONGODB_DIR=${1}
if [ ! -x "${MONGODB_DIR}/bin/mongod" ]; then
    echo "Error: MongoDB directory is incorrect"
    usage
    exit 1
fi

DATA_DIR=${2}
if [ ! -d "${DATA_DIR}/mongodb_data" ]; then
    echo "Error: Missing ${DATA_DIR}/mongodb_data"
    usage
    exit 1
fi

# Setup our data directory info
DBLOCATION="${DATA_DIR}/mongodb_data"

echo "Start: Launching MongoDB..."
sleep 1 # Wait just a second for any previous instance to clear up
${MONGODB_DIR}/bin/mongod --fork --dbpath="${DBLOCATION}" --logpath="${DBLOCATION}/mongodb.log"
if [ $? -ne 0 ]; then
    echo "Error: Failed to start MongoDB"
    exit 1
fi
echo "Start: Started MongoDB"

exit 0
