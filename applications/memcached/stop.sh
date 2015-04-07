#!/bin/bash

usage() {
    echo "Usage: stop.sh MEMCACHED_DIR DATA_DIR INSTANCE PID_FILE"
}

if [ $# -ne 4 ]; then
    usage
    exit 1
fi

PID_FILE=${4}

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
