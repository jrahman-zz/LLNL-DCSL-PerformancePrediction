#!/bin/bash

usage() {
    echo "Usage: run.sh SPEC_DIR DATA_DIR INSTANCE BMARK_NAME SIZE INTERFERENCE"
}

if [ $# -ne 6 ]; then
    usage
    exit 1
fi

HOSTNAME=`hostname`

SPEC_DIR=${1}
DATA_DIR=${2}
INSTANCE=${3}
BMARK_NAME=${4}
SIZE=${5}
INTERFERENCE=${6}

BASE_DIR=$(dirname $0)/

echo "Run: Starting now..."
(
    cd "${SPEC_DIR}"
    source shrc
    if [ "x${INTERFERENCE}" == "x1" ]; then 
        TARGET="${SPEC_DIR}/benchspec/CPU2006/${BMARK_NAME}/run/run_base_${SIZE}_${HOSTNAME}_${INSTANCE}.0000"
		./bin/specinvoke -d "${TARGET}"
    else
        ./bin/runspec -c custom-linux64.cfg --nobuild --iterations 1 --noreportable --define HOSTNAME=${HOSTNAME} --define INSTANCE=${INSTANCE} --size ${SIZE} --action run "${BMARK_NAME}"
    fi
)
if [ $? -ne 0 ]; then
    echo "Error: Failed to run the benchmark"
    exit 2
fi
echo "Run: Completed"

exit 0
