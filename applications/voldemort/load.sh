#!/bin/bas

usage() {
    echo "Usage: load.sh YCSB_DIR VOLDEMORT_DIR DATA_DIR"
}

if [ $# -ne 3 ]; then
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
VOLDEMORT_DIR=${2}
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
DATA_DIR=${3}
if [ ! -d "${DATA_DIR}" ]; then
    echo "Error: Data parent directory doesn't exist"
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

echo "Load: Starting server..."
# TODO, change this to voldemort-prod-server.sh
${VOLDEMORT_DIR}/bin/voldemort-server.sh "${DBLOCATION}" "${VOLDEMORT_DIR}/config/single_node_cluster/config/" &> /dev/null &
if [ $? -ne 0 ]; then
    echo "Error: Failed to start Voldemort"
    exit 1
fi

# Short sleep so the server can start
sleep 3

# Health check the server and ping away
${VOLDEMORT_DIR}/bin/voldemort-admin-tool.sh --ro-metadata current --url tcp://localhost:6666 --node 0 &> /dev/null
if [ $? -ne 0 ]; then
    echo "Error: Failed to start Voldemort"
    exit 1
fi
echo "Load: Started Voldemort"

# Load the data as needed
echo "Load: Loading data into Voldemort"
${YCSB_DIR}/bin/ycsb load voldemort -P "${YCSB_DIR}/workloads/workloada" -threads 4 -P "workload.dat" -p "boostrap_urls=[tcp://localhost:6666]" -s
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
