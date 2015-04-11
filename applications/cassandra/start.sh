#!/bin/bash

usage() {
    echo "Usage: start.sh CASSANDRA_HOME DATA_DIR INSTANCE PIDFILE CASSANDRA_INCLUDE"
}

if [ $# -ne 5 ]; then
    usage
    exit 1
fi

CASSANDRA_DIR=${1}
if [ ! -x "${CASSANDRA_DIR}/bin/cassandra" -o ! -x "${CASSANDRA_DIR}/bin/nodetool" ]; then
    echo "Error: Cassandra directory is incorrect"
    usage
    exit 2
fi

DATA_DIR=${2}
if [ ! -d "${DATA_DIR}/cassandra_data" ]; then
    echo "Error: Missing ${DATA_DIR}/cassandra_data"
    usage
    exit 3
fi
export DATA_DIR

INSTANCE=${3}
PID_FILE=${4}

CASSANDRA_INCLUDE=${5}
if [ ! -r "${CASSANDRA_INCLUDE}" ]; then
    echo "Error: Bad cassandra include config file"
    usage
    exit 4
fi
export CASSANDRA_INCLUDE

echo "Start: Launching Cassandra..."
${CASSANDRA_DIR}/bin/cassandra -p "${PID_FILE}" &> /dev/null
if [ $? -ne 0 ]; then
    echo "Error: Failed to start server"
    exit 5
fi

# Give the server some time to start
ALIVE=0
for I in `seq 5`; do
    echo "Start: Sleeping to give Cassandra time to start..."
    sleep 5
    echo "Start: Woke up, health check..."
    ${CASSANDRA_DIR}/bin/nodetool status &> /dev/null
    if [ $? -eq 0 ]; then
        ALIVE=1
        break
    fi
done

if [ ${ALIVE} -ne 1 ]; then
    echo "Error: Failed to start Cassandra server"
    exit 6
fi
echo "Start: Cassandra alive"

exit 0
