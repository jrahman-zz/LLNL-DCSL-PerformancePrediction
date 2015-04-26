#!/bin/bash

usage() {
    echo "Usage: run.sh PARSEC_DIR DATA_DIR INSTANCE BMARK_NAME SIZE NTHREADS"
}

if [ $# -ne 6 ]; then
    usage
    exit 1
fi

PARSEC_DIR=${1}
DATA_DIR=${2}
INSTANCE=${3}
BMARK_NAME=${4}
SIZE=${5}
export NTHREADS=${6}
export OMP_NUM_THREADS=${NTHREADS}

BASE_DIR=$(dirname $0)/

if [ "x${BMARK_NAME}" == "x" ]; then
	echo "Error: Bad benchmark name"
	exit 1
fi

if [ "${SIZE}" != "simsmall" ] && [ "${SIZE}" != "simmedium" ] && [ "${SIZE}" != "simlarge" ] && [ "${SIZE}" != "native" ]; then
    echo "Error: Bad input size \"${SIZE}\""
    exit 2
fi

echo "${NTHREADS}" | grep "[0-9]" > /dev/null
if [ $? -ne 0 ]; then
    echo "Error: Invalid NTHREADS \"${NTHREADS}\""
    exit 3
fi

echo "Run: Starting now..."
"${PARSEC_DIR}/bin/parsecmgmt" -a run -d "${DATA_DIR}" -i "${SIZE}" -n "${NTHREADS}" -p "${BMARK_NAME}"
if [ $? -ne 0 ]; then
    echo "Error: Failed to run the benchmark"
    exit 4
fi
echo "Run: Completed"

exit 0
