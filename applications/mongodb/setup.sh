#!/bin/bash


usage() {
    echo "Usage: setup.sh YCSB_DIR MONGODB_DIR DATA_DIR PID_FILE"
}

if [ $# -ne 4 ]; then
    usage
    exit 1
fi

# Path to base of YCSB dir
YCSB_DIR=${1}
if [ ! -d "${YCSB_DIR}" ]; then
    echo "Error: YCSB directory doesn't exist"
    usage
    exit 1
fi

if [ ! -x "${YCSB_DIR}/bin/ycsb" ]; then
    echo "Error: YCSB directory is incorrect"
    usage
    exit 1
fi

# Path
MONGODB_DIR=${2}
if [ ! -d "${MONGODB_DIR}" ]; then
    echo "Error: MongoDB directory doesn't exist"
    usage
    exit 1
fi

if [ ! -f "${MONGODB_DIR}/bin/mongod" ]; then
    echo "Error: MongoDB directory is incorrect"
    usage
    exit 1
fi

# Path to directory to store data directory
DATA_DIR=${3}
if [ ! -d "${DATA_DIR}" ]; then
    echo "Error: Data parent directory doesn't exist"
    usage
    exit 1
fi

# Name of PID file
PID_FILE=${4}

# Delete old datadir
if [ -d "${DATA_DIR}/mongodb_data" ]; then
    echo "Setup: Deleting old data directory at ${DATA_DIR}/mongodb_data..."
    rm -rf "${DATA_DIR}/mongodb_data"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to delete ${DATA_DIR}/mongodb_data"
        exit 1
    fi
    echo "Setup: Deleted old data directory"
fi

# Create new, empty data directory on target drive
echo "Setup: Creating new data directory at ${DATA_DIR}/mongodb_data..."
mkdir -p "${DATA_DIR}/mongodb_data"
if [ $? -ne 0 ]; then
    echo "Error: Failed to create data directory"
    exit 1
fi
echo "Setup: Created data directory"

# Tweak the config file...
echo "Setup: Customizing configuration..."
cp "config.yaml" "config.yaml.custom"
if [ $? -ne 0 ]; then
    echo "Error: Failed to copy config"
    exit 1
fi

DBLOCATION="${DATA_DIR}/mongodb_data/"

echo "Setup: Starting server..."
${MONGODB_DIR}/bin/mongod --pidfilepath "${PIDFILE}" --fork --dbpath="${DBLOCATION}" --logpath="${DBLOCATION}/mongodb.log"
if [ $? -ne 0 ]; then
    echo "Error: Failed to start mongodb"
    exit 1
fi

# Give MongoDB time to catch it's breath
echo "Setup: Waiting for MongoDB to start..."
sleep 10
echo "Setup: Waking up from deep sleep"

# Create our database
echo "Setup: Creating database..."
${MONGODB_DIR}/bin/mongo setup.js
if [ $? -ne 0 ]; then
    echo "Error: Failed to setup database"
    exit 1
fi

# Load the data as needed
echo "Setup: Loading data into MongoDB"
${YCSB_DIR}/bin/ycsb load mongodb -P "${YCSB_DIR}/workloads/workloada" -threads 4
if [ $? -ne 0 ]; then
    echo "Error: Failed to load data into MongoDB"
    exit 1
fi
echo "Setup: Loaded data into MongoDB"

exit 0
