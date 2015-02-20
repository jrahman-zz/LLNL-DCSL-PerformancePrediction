#!/bin/bash

usage() {
    echo "Usage: run.sh SPEC_DIR DATA_DIR BMARK_NAME SIZE"
}

if [ $# -ne 4 ]; then
    usage
    exit 1
fi

SPEC_DIR=${1}
DATA_DIR=${2}
BMARK_NAME=${3}
SIZE=${4}

BASE_DIR=$(dirname $0)/

echo "Run: Starting now..."
(
    cd "${SPEC_DIR}"
    source shrc
    ./bin/runspec -c custom-linux64.cfg --nobuild --iterations 1 --noreportable --size ${SIZE} --action run "${BMARK_NAME}"
    )
if [ $? -ne 0 ]; then
    echo "Error: Failed to run the benchmark"
    exit 1
fi
echo "Run: Completed"

exit 0
