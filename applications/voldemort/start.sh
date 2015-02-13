#!/bin/bash

usage() {
    echo "Usage: start.sh MONGO_HOME DATA_DIR PIDFILE"
}

if [ $# -ne 3 ]; then
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

PID_FILE=${4}

# Setup our data directory info
DBLOCATION="${DATA_DIR}/mongodb_data"

echo "Start: Launching MongoDB..."
${MONGODB_DIR}/bin/mongod --pidfilepath="${PID_FILE}" --fork --dbpath="${DBLOCATION}" --logpath="${DBLOCATION}.mongodb.log"
if [ $? -ne 0 ]; then
    echo "Error: Failed to start MongoDB"
    exit 1
fi
echo "Start: Started MongoDB"

exit 0
