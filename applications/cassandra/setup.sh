#!/bin/bash

usage() {
    echo "Usage: setup.sh YCSB_DIR CASSANDRA_DIR DATA_DIR CASSANDRA_INCLUDE PID_FILE"
}

if [ $# -ne 5 ]; then
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
CASSANDRA_DIR=${2}
if [ ! -d "${CASSANDRA_DIR}" ]; then
    echo "Error: Cassandra directory doesn't exist"
    usage
    exit 1
fi

if [ ! -f "${CASSANDRA_DIR}/bin/cassandra" -o ! -x "${CASSANDRA_DIR}/bin/cassandra-cli" ]; then
    echo "Error: Cassandra directory is incorrect"
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
export DATA_DIR

CASSANDRA_INCLUDE=${4}
if [ ! -r "${CASSANDRA_INCLUDE}" ]; then
    echo "Error: Bad cassandra include config file"
    usage
    exit 1
fi
export CASSANDRA_INCLUDE

# Name of PID file
PID_FILE=${5}

# Delete old datadir
if [ -d "${DATA_DIR}/cassandra_data" ]; then
    echo "Setup: Deleting old data directory at ${DATA_DIR}/cassandra_data..."
    rm -rf "${DATA_DIR}/cassandra_data"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to delete ${DATA_DIR}/cassandra_data"
        exit 1
    fi
    echo "Setup: Deleted old data directory"
fi

# Create new, empty data directory on target drive
echo "Setup: Creating new data directory at ${DATA_DIR}/cassandra_data..."
mkdir -p "${DATA_DIR}/cassandra_data"
if [ $? -ne 0 ]; then
    echo "Error: Failed to create data directory"
    exit 1
fi
echo "Setup: Created data directory"

# Start the server in the background
echo "Setup: Starting server"
${CASSANDRA_DIR}/bin/cassandra -p "${PID_FILE}" > test.out
if [ $? -ne 0 ]; then
    echo "Error: Failed to start server"
    exit 1
fi

# Need to give the server a couple seconds to catch it's breath...
echo "Setup: Sleeping to give Cassandra time to start..."
sleep 30
echo "Setup: Woke up, time to prepare data..."

# Ok, lets build the tables
echo "Setup: Creating tables..."
${CASSANDRA_DIR}/bin/cassandra-cli -h 127.0.0.1 -f setup.cql
if [ $? -ne 0 ]; then
    echo "Error: Failed to create table"
    exit 1
fi
echo "Setup: Tables created"


# And now we load the benchmark data
echo "Setup: Loading data..."
${YCSB_DIR}/bin/ycsb load cassandra-10 -threads 4 -P "${YCSB_DIR}/workloads/workloada" -p hosts="127.0.0.1"
if [ $? -ne 0 ]; then
    echo "Error: Failed to load test data"
    exit 1
fi
echo "Setup: Data loaded"

exit 0
