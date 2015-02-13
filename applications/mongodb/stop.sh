#!/bin/bash

usage() {
    echo "Usage: stop.sh MONGODB_DIR DATA_DIR"
}

if [ $# -ne 2 ]; then
    usage
    exit 1
fi

MONGODB_DIR="${1}"
if [ ! -d "${MONGODB_DIR}" -o ! -x "${MONGODB_DIR}/bin/mongod" ]; then
    echo "Error: Bad MongoDB directory"
    usage
    exit 1
fi

DATA_DIR="${2}"
DBLOCATION="${DATA_DIR}/mongodb_data"
if [ ! -d "${DBLOCATION}" ]; then
    echo "Error: ${DBLOCATION} doesn't exist"
    exit 1
fi


${MONGODB_DIR}/bin/mongod --shutdown --dbpath="${DBLOCATION}"
exit ${SUCCESS}
