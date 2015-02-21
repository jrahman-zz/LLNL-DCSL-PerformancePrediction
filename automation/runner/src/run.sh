#!/bin/bash

usage() {
    echo "Usage: run.sh INSTANCES INTEFERENCE DATA_BASE APPLICATION_BASE"
}

if [ $# -ne 4 ]; then
    usage
    exit 1
fi

INSTANCES=${1}
INTERFERENCE=${2}
DATA_BASE={$3}
APPLICATION_BASE=${4}

BASE_DIR=$(dirname $0)
SOURCE_BASE="${BASE_DIR}/../../../"

# Build customize json files
cp "${BASE_DIR}/config.json.template" "${BASE_DIR}/config.json"
cp "${BASE_DIR}/applications.json.template" "${BASE_DIR}/applications.json"
cp "${BASE_DIR}/benchmarks.json.template" "${BASE_DIR}/benchmarks.json"

DATA_BASE="/tmp/applications/"
PATTERN="s \\\${DATA_BASE} ${DATA_BASE} g"
echo "${PATTERN}"
sed -i "${PATTERN}" "${BASE_DIR}/config.json" "${BASE_DIR}/applications.json"
if [ $? -ne 0 ]; then
    echo "Failed to build JSON files"
    exit 2
fi

SOURCE_BASE="/home/jprahman/LLNL-DCSL-PerformancePrediction/"
PATTERN="s \\\${SOURCE_BASE} ${SOURCE_BASE} g"
echo "${PATTERN}"
sed -i "${PATTERN}" "${BASE_DIR}/config.json" "${BASE_DIR}/applications.json"
if [ $? -ne 0 ]; then
    echo "Failed to build JSON files"
    exit 3
fi

APPLICATION_BASE="/home/jprahman/llnl/"
PATTERN="s \\\${APPLICATION_BASE} ${APPLICATION_BASE} g"
echo "${PATTERN}"
sed -i "${PATTERN}" "${BASE_DIR}/config.json" "${BASE_DIR}/applications.json"
if [ $? -ne 0 ]; then
    echo "Failed to build JSON files"
    exit 4
fi

# Build data dir
mkdir -p "${DATA_BASE}"
if [ $? -ne 0 ]; then
    echo "Failed to build data base directory"
    exit 5
fi

# Build temp files and directories for the benchmark
for INSTANCE in `seq ${INSTANCES}`; do
    mkdir -p "${DATA_BASE}/metadata.${INSTANCE}"
    if [ $? -ne 0 ]; then
        echo "Failed to create ${DATA_BASE}/metadata.${INSTANCE}"
        exit 6
    fi

    FILE="${DATA_BASE}/iobench.${INSTANCE}"
    echo "${SOURCE_BASE}/benchmarks/bin"
    java -classpath "${SOURCE_BASE}/benchmarks/bin/iobench.jar" Main create "${FILE}" 256M
    if [ $? -ne 0 ]; then
        echo "Failed to create ${FILE}"
        exit 7
    fi
done


