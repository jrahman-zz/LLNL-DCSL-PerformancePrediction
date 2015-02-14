#!/bin/bash

usage() {
    echo "Usage: load.sh CASSANDRA_DIR DATA_DIR YCSB_DIR PID_FILE CASSANDRA_INCLUDE"
}

if [ $# -ne 5 ]; then
    usage
    exit 1
fi

# Path
CASSANDRA_DIR=${1}
if [ ! -d "${CASSANDRA_DIR}" ]; then
    echo "Error: Cassandra directory doesn't exist"
    usage
    exit 1
fi

if [ ! -x "${CASSANDRA_DIR}/bin/cassandra" -o ! -x "${CASSANDRA_DIR}/bin/cassandra-cli" ]; then
    echo "Error: Cassandra directory is incorrect"
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
export DATA_DIR

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

# Name of PID file
PID_FILE=${4}

CASSANDRA_INCLUDE=${5}
if [ ! -r "${CASSANDRA_INCLUDE}" ]; then
    echo "Error: Bad cassandra include config file"
    usage
    exit 1
fi
export CASSANDRA_INCLUDE

# Delete old datadir
if [ -d "${DATA_DIR}/cassandra_data" ]; then
    echo "Load: Deleting old data directory at ${DATA_DIR}/cassandra_data..."
    rm -rf "${DATA_DIR}/cassandra_data"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to delete ${DATA_DIR}/cassandra_data"
        exit 1
    fi
    echo "Load: Deleted old data directory"
fi

# Create new, empty data directory on target drive
echo "Load: Creating new data directory at ${DATA_DIR}/cassandra_data..."
mkdir -p "${DATA_DIR}/cassandra_data"
if [ $? -ne 0 ]; then
    echo "Error: Failed to create data directory"
    exit 1
fi
echo "Load: Created data directory"

# Start the server in the background
echo "Load: Starting server"
${CASSANDRA_DIR}/bin/cassandra -p "${PID_FILE}" &> test.out
if [ $? -ne 0 ]; then
    echo "Error: Failed to start server"
    exit 1
fi

# Need to give the server a couple seconds to catch it's breath...
echo "Load: Sleeping to give Cassandra time to start..."
sleep 30
echo "Load: Woke up, time to prepare data..."

# Ok, lets build the tables
echo "Load: Creating tables..."
${CASSANDRA_DIR}/bin/cassandra-cli -h 127.0.0.1 -f setup.cql
if [ $? -ne 0 ]; then
    echo "Error: Failed to create table"
    exit 1
fi
echo "Load: Tables created"

# And now we load the benchmark data
echo "Load: Loading data..."
${YCSB_DIR}/bin/ycsb load cassandra-10 -threads 4 -P "${YCSB_DIR}/workloads/workloada" -p "recordcount=1000000" -p hosts="127.0.0.1"
if [ $? -ne 0 ]; then
    echo "Error: Failed to load test data"
    exit 1
fi
echo "Load: Data loaded"

sleep 10

echo "Load: Shutting Cassandra down..."
kill `cat ${PID_FILE}`
if [ $? -ne 0 ]; then
    echo "Error: Failed to shut Cassandra down"
    exit 1
fi
echo "Load: Shut Cassandra down"

exit 0
