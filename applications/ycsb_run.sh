#!/bin/bash

usage() {
    echo "Usage: run.sh YCSB_DIR DATABASE [EXTRA_PARAMS]"
}

if [ $# -lt 2 ]; then
    usage
    exit 1
fi

YCSB_DIR=${1}
if [ ! -x "${YCSB_DIR}/bin/ycsb" -o ! -d "${YCSB_DIR}/workloads" ]; then
    echo "Error: Bad YCSB directory"
    usage
    exit 1
fi

DATABASE=${2} # TODO, should we sanity check this?

# Shift both required parameters away
shift 2

WORKLOADS="${YCSB_DIR}/workloads/workload"{a,b,c,d}


PARAMS='-P workload.dat'

# Loop over each possible workload
for WORKLOAD in ${WORKLOADS}; do
    echo "Run: Running workload ${WORKLOAD}..."
    ${YCSB_DIR}/bin/ycsb run "${DATABASE}" -P "${WORKLOAD}" "${PARAMS}" $@
    if [ $? -ne 0 ]; then
        echo "Error: Workload ${WORKLOAD} failed"
        exit 1
    fi
done

exit 0
