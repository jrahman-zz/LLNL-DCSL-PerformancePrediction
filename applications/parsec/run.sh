#!/bin/bash

usage() {
    echo "Usage: run.sh PARSEC_DIR DATA_DIR BMARK_NAME SIZE NTHREADS"
}

if [ $# -ne 5 ]; then
    usage
    exit 1
fi

PARSEC_DIR=${1}
DATA_DIR=${2}
BMARK_NAME=${3}
SIZE=${4}
export NTHREADS=${5}
export OMP_NUM_THREADS=${NTHREADS}

BASE_DIR=$(dirname $0)/

if [ "${SIZE}" != "simsmall" ] && [ "${SIZE}" != "simmedium" ] && [ "${SIZE}" != "simlarge" ] && [ "${SIZE}" != "native" ]; then
    echo "Error: Bad input size \"${SIZE}\""
    exit 1
fi

echo "${NTHREADS}" | grep "[0-9]" > /dev/null
if [ $? -ne 0 ]; then
    echo "Error: Invalid NTHREADS \"${NTHREADS}\""
    exit 2
fi

echo "Run: Starting now..."
"${PARSEC_DIR}/bin/parsecmgmt" -a run -p "${BMARK_NAME}" -d "${DATA_DIR}" -i "${SIZE}" -n "${NTHREADS}"
if [ $? -ne 0 ]; then
    echo "Error: Failed to run the benchmark"
    exit 3
fi
echo "Run: Completed"

exit 0
