#!/bin/bash

usage() {
    echo "Usage: stop.sh CASSANDRA_DIR DATA_DIR PID_FILE"
}

if [ $# -ne 3 -o ! -r "${3}" ]; then
    # Ignore first two parameters
    echo "Error: Bad pid file"
    usage
    exit 1
fi

PID=`cat "${3}"`
echo "Stop: Killing proces with PID ${PID}"
kill "${PID}"
SUCCESS=$?

# Take out the trash
if [ -f "${3}" ]; then
    rm "${3}"
fi

if [ ${SUCCESS} -eq 0 ]; then
    echo "Stop: Stopped Cassandra"
fi

exit ${SUCCESS}
