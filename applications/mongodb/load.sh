#!/bin/bash


usage() {
    echo "Usage: load.sh MONGODB_DIR DATA_DIR YCSB_DIR"
}

if [ $# -ne 3 ]; then
    usage
    exit 1
fi

# Path
MONGODB_DIR=${1}
if [ ! -d "${MONGODB_DIR}" ]; then
    echo "Error: MongoDB directory doesn't exist"
    usage
    exit 1
fi

if [ ! -x "${MONGODB_DIR}/bin/mongod" ]; then
    echo "Error: MongoDB directory is incorrect"
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

# Path to base of YCSB dir
YCSB_DIR=${3}
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


# Delete old datadir
if [ -d "${DATA_DIR}/mongodb_data" ]; then
    echo "Load: Deleting old data directory at ${DATA_DIR}/mongodb_data..."
    rm -rf "${DATA_DIR}/mongodb_data"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to delete ${DATA_DIR}/mongodb_data"
        exit 1
    fi
    echo "Load: Deleted old data directory"
fi

# Create new, empty data directory on target drive
echo "Load: Creating new data directory at ${DATA_DIR}/mongodb_data..."
mkdir -p "${DATA_DIR}/mongodb_data"
if [ $? -ne 0 ]; then
    echo "Error: Failed to create data directory"
    exit 1
fi
echo "Load: Created data directory"

DBLOCATION="${DATA_DIR}/mongodb_data/"

echo "Load: Starting server..."
${MONGODB_DIR}/bin/mongod --fork --dbpath="${DBLOCATION}" --logpath="${DBLOCATION}/mongodb.log"
if [ $? -ne 0 ]; then
    echo "Error: Failed to start mongodb"
    exit 1
fi

# Create our database
echo "Load: Creating database..."
${MONGODB_DIR}/bin/mongo setup.js
if [ $? -ne 0 ]; then
    echo "Error: Failed to setup database"
    exit 1
fi

# Load the data as needed
echo "Load: Loading data into MongoDB"
${YCSB_DIR}/bin/ycsb load mongodb -P "${YCSB_DIR}/workloads/workloada" -threads 4 -p "recordcount=1000000"
if [ $? -ne 0 ]; then
    echo "Error: Failed to load data into MongoDB"
    exit 1
fi
echo "Load: Loaded data into MongoDB"

echo "Load: Shutting MongoDB down..."
${MONGODB_DIR}/bin/mongod --shutdown --dbpath="${DBLOCATION}"
if [ $? -ne 0 ]; then
    echo "Error: Failed to stop MongoDB"
    exit 1
fi

# Give MongoDB some time to release resources and locks
sleep 2
echo "Load: Shutdown MongoDB"

exit 0
