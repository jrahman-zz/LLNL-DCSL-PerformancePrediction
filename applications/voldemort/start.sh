#!/bin/bash

usage() {
    echo "Usage: start.sh VOLDEMORT_HOME DATA_DIR PIDFILE"
}

if [ $# -ne 3 ]; then
    usage
    exit 1
fi

VOLDEMORT_DIR=${1}
if [ ! -x "${VOLDEMORT_DIR}/bin/voldemort-server.sh" ]; then
    echo "Error: Voldemort directory is incorrect"
    usage
    exit 1
fi

DATA_DIR=${2}
if [ ! -d "${DATA_DIR}/voldemort_data" ]; then
    echo "Error: Missing ${DATA_DIR}/voldemort_data"
    usage
    exit 1
fi

PID_FILE=${4}

# Setup our data directory info
DBLOCATION="${DATA_DIR}/voldemort_data"

echo "Start: Launching Voldemort..."
${VOLDEMORT_DIR}/bin/voldemort-server.sh
if [ $? -ne 0 ]; then
    echo "Error: Failed to start Voldemort"
    exit 1
fi
echo "Start: Started Voldemort"

exit 0
