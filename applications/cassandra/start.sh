#!/bin/bash

usage() {
    echo "Usage: start.sh CASSANDRA_HOME DATA_DIR CASSANDRA_INCLUDE PIDFILE"
}

if [ $# -ne 4 ]; then
    usage
    exit 1
fi

CASSANDRA_DIR=${1}
if [ ! -x "${CASSANDRA_DIR}/bin/cassandra" -o ! -x "${CASSANDRA_DIR}/bin/nodetool" ]; then
    echo "Error: Cassandra directory is incorrect"
    usage
    exit 1
fi

DATA_DIR=${2}
if [ ! -d "${DATA_DIR}/cassandra_data" ]; then
    echo "Error: Missing ${DATA_DIR}/cassandra_data"
    usage
    exit 1
fi
export DATA_DIR

CASSANDRA_INCLUDE=${3}
if [ ! -r "${CASSANDRA_INCLUDE}" ]; then
    echo "Error: Bad cassandra include config file"
    usage
    exit 1
fi
export CASSANDRA_INCLUDE

PID_FILE=${4}

echo "Start: Launching Cassandra..."
${CASSANDRA_DIR}/bin/cassandra -p "${PID_FILE}" &> /dev/null
if [ $? -ne 0 ]; then
    echo "Error: Failed to start server"
    exit 1
fi

# Give the server some time to start
ALIVE=0
for I in `seq 1`; do
    echo "Start: Sleeping to give Cassandra time to start..."
    sleep 5
    echo "Start: Woke up, health check..."
    ${CASSANDRA_DIR}/bin/nodetool status &> /dev/null
    if [ $? -eq 0 ]; then
        ALIVE=1
    fi
done

if [ ${ALIVE} -ne 1 ]; then
    echo "Error: Failed to start Cassandra server"
    exit 1
fi

exit 0
