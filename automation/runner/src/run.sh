#!/bin/bash

usage() {
    echo "Usage: run.sh INSTANCES INTEFERENCE APPS MODE OUTPUT_PATH DATA_BASE APP_BASE"
}

if [ $# -ne 7 ]; then
    usage
    exit 1
fi


INSTANCES=${1} # For multi-instance application and benchmark support
INTERFERENCE=${2}
APPS=${3}
MODE=${4} # Testing or training
OUTPUT_PATH=${5}
DATA_BASE=${6}
APP_BASE=${7}

BASE_DIR=$(dirname $0)
SOURCE_BASE="${BASE_DIR}/../../../"

# Build customize json files
cp "${BASE_DIR}/config.json.template" config.json
cp "${BASE_DIR}/applications.json.template" applications.json
cp "${BASE_DIR}/benchmarks.json.template" benchmarks.json
cp "${BASE_DIR}/interference.json.${MODE}" interference.json

PATTERN="s \\\${DATA_BASE} ${DATA_BASE} g"
echo "${PATTERN}"
sed -i "${PATTERN}" config.json applications.json interference.json

if [ $? -ne 0 ]; then
    echo "Failed to build JSON files"
    exit 2
fi

PATTERN="s \\\${SOURCE_BASE} ${SOURCE_BASE} g"
echo "${PATTERN}"
sed -i "${PATTERN}" config.json applications.json interference.json

if [ $? -ne 0 ]; then
    echo "Failed to build JSON files"
    exit 3
fi

PATTERN="s \\\${APPLICATION_BASE} ${APP_BASE} g"
echo "${PATTERN}"
sed -i "${PATTERN}"  config.json applications.json interference.json

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

echo "Starting run..."
python ${BASE_DIR}/run.py --applications "${APPS}" --interference "${INTERFERENCE}" --output ${OUTPUT_PATH} --config "${BASE_DIR}/config.json"
if [ $? -ne 0 ]; then
    echo "Run failed"
    exit 8
fi

echo "Cleaning up data directory: ${DATA_BASE}"
rm -rf "${DATA_BASE}"
if [ $? -ne 0 ]; then
    echo "Failed to cleanup data directory"
    exit 9
fi

exit 0
