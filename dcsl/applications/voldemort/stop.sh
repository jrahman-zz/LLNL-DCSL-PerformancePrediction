#!/bin/bash

# TODO, update parameters

if [ $# -ne 1 -o ! -r "${1}" ]; then
    echo "Error: Bad pid file"
    exit 1
fi

PID=`cat "${1}"`
echo "Stop: Killing proces with PID ${PID}"
kill "${PID}"
SUCCESS=$?

# Take out the trash
if [ -f "${1}" ]; then
    rm "${1}"
fi
exit ${SUCCESS}
