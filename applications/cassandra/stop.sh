#!/bin/bash

usage() {
    echo "Usage: stop.sh CASSANDRA_DIR DATA_DIR INSTNACE PID_FILE"
}

if [ $# -ne 4 -o ! -r "${4}" ]; then
    # Ignore first three parameters
    echo "Error: Bad pid file"
    usage
    exit 1
fi

PID=`cat "${4}"`
echo "Stop: Killing proces with PID ${PID}"
kill "${PID}"
SUCCESS=$?

# Take out the trash
if [ -f "${4}" ]; then
    rm "${4}"
fi

if [ ${SUCCESS} -eq 0 ]; then
    echo "Stop: Stopped Cassandra"
fi

exit ${SUCCESS}
