#!/bin/bash

usage() {
    echo "Usage: stop.sh MEMCACHED_DIR DATA_DIR PID_FILE"
}

if [ $# -ne 3 ]; then
    usage
    exit 1
fi

if [ ! -r "${PID_FILE}" -o `wc -l ${PID_FILE}` -ne 1 ]; then
    echo "Bad PID file"
    usage
    exit 1
fi

kill `cat ${PID_FILE}`
if [ $? -ne 0 ]; then
    echo "Error: Failed to shutdown memcached"
fi
rm "${PID_FILE}"

exit 0
