#!/bin/bash

usage() {
    echo "Usage: run.sh SPEC_DIR DATA_DIR BMARK_NAME SIZE INTERFERENCE"
}

if [ $# -ne 5 ]; then
    usage
    exit 1
fi

SPEC_DIR=${1}
DATA_DIR=${2}
BMARK_NAME=${3}
SIZE=${4}
INTERFERENCE=${5}

BASE_DIR=$(dirname $0)/

echo "Run: Starting now..."
(
    cd "${SPEC_DIR}"
    source shrc
    if [ "x${INTERFERENCE}" == "x1" ]; then 
        ./bin/specinvoke -d "${SPEC_DIR}/benchspec/CPU2006/${BMARK_NAME}/run/run_base_${SIZE}_x86-64.0001"
    else
        ./bin/runspec -c custom-linux64.cfg --nobuild --iterations 1 --noreportable --size ${SIZE} --action run "${BMARK_NAME}"
    fi
)
if [ $? -ne 0 ]; then
    echo "Error: Failed to run the benchmark"
    exit 2
fi
echo "Run: Completed"

exit 0
