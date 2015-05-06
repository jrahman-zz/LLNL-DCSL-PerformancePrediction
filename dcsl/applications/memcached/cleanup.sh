#!/bin/bash

usage() {
    echo "Usage: cleanup.sh MEMCACHED_DIR DATA_DIR INSTANCE"
}

if [ $# -ne 3 ]; then
    echo "Error: Invalid arguements"
    usage
    exit 1
fi

DATA_DIR="${3}/memcached_data"
if [ -d "${DATA_DIR}" ]; then
    echo "Cleanup: Removing ${DATA_DIR}..."
    rm -rf "${DATA_DIR}"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to cleanup data"
        exit 1
    fi
    echo "Cleanup: Removed ${DATA_DIR}"
fi

exit 0
