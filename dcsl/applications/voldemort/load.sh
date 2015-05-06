#!/bin/bash

usage() {
    echo "Usage: load.sh VOLDEMORT_DIR DATA_DIR INSTANCE YCSB_DIR"
}

if [ $# -ne 4 ]; then
    usage
    exit 1
fi

# Path
VOLDEMORT_DIR=${1}
if [ ! -d "${VOLDEMORT_DIR}" ]; then
    echo "Error: Voldemort directory doesn't exist"
    usage
    exit 1
fi

if [ ! -x "${VOLDEMORT_DIR}/bin/voldemort-server.sh" -o ! -x "${VOLDEMORT_DIR}/bin/voldemort-stop.sh" ]; then
    echo "Error: Voldemort directory is incorrect"
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

INSTANCE=${3}

# Path to base of YCSB dir
YCSB_DIR=${4}
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
if [ -d "${DATA_DIR}/voldemort_data" ]; then
    echo "Load: Deleting old data directory at ${DATA_DIR}/voldemort_data..."
    rm -rf "${DATA_DIR}/voldemort_data"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to delete ${DATA_DIR}/voldemort_data"
        exit 1
    fi
    echo "Setup: Deleted old data directory"
fi

# Create new, empty data directory on target drive
echo "Load: Creating new data directory at ${DATA_DIR}/voldemort_data..."
mkdir -p "${DATA_DIR}/voldemort_data"
if [ $? -ne 0 ]; then
    echo "Error: Failed to create data directory"
    exit 1
fi
echo "Load: Created data directory"


DBLOCATION="${DATA_DIR}/voldemort_data/"

# Copy the config to the new home dir location
echo "Load: Copying configuration files..."
cp -r "${VOLDEMORT_DIR}/config/single_node_cluster/config" "${DBLOCATION}"
if [ $? -ne 0 ]; then
    echo "Error: Failed to copy configuration files"
    exit 1
fi
echo "Load: Copied configuration files"

echo "Load: Starting server..."
# TODO, change this to voldemort-prod-server.sh
${VOLDEMORT_DIR}/bin/voldemort-server.sh "${DBLOCATION}" &> /dev/null &
if [ $? -ne 0 ]; then
    echo "Error: Failed to start Voldemort"
    exit 1
fi

# Short sleep so the server can start
sleep 3

# Health check the server and ping away
${VOLDEMORT_DIR}/bin/voldemort-admin-test.sh -f -n 0 tcp://localhost:6666 test
if [ $? -ne 0 ]; then
    echo "Error: Failed to start Voldemort"
    exit 1
fi
echo "Load: Started Voldemort"

# Load the data as needed
echo "Load: Loading data into Voldemort"
${YCSB_DIR}/bin/ycsb load voldemort -P "${YCSB_DIR}/workloads/workloada" -threads 4 -P "workload.dat" -p "bootstrap_urls=tcp://localhost:6666,tcp://localhost:6666" -s
if [ $? -ne 0 ]; then
    echo "Error: Failed to load data into Voldemort"
    exit 1
fi
echo "Load: Loaded data into Voldemort"

# Give Voldemort a couple seconds to cool down, flush caches, etc before shutting down
sleep 5

echo "Load: Shutting Voldemort down..."
${VOLDEMORT_DIR}/bin/voldemort-stop.sh
if [ $? -ne 0 ]; then
    echo "Error: Failed to stop Voldemort"
    exit 1
fi
echo "Load: Shutdown Voldemort"

exit 0
