#!/bin/bash


#
# Performs setup for a given run
# 
# 1. Copies configs and replaces placeholders
# 2. Creates empty folders for metadata benchmark (if needed)
# 3. Creates benchmark files for IOBench (if needed)
#

usage() {
    echo "Usage: setup.sh INSTANCES CONFIG INTERFERENCE_CONFIG BENCHMARK_CONFIG APP_CONFIG DATA_BASE APP_BASE"
}

if [ $# -ne 7 ]; then
    usage
    exit 1
fi

INSTANCES=${1} # For multi-instance application and benchmark support
CONFIG=${2}
INTERFERENCE_CONFIG=${3}
BENCHMARK_CONFIG=${4}
APP_CONFIG=${5}
DATA_BASE=${6}
APP_BASE=${7}

BASE_DIR=$(dirname $0)
SOURCE_BASE="${BASE_DIR}"

echo "Source Base: ${SOURCE_BASE}"

# Build customize json files
cp "${CONFIG}" config.json
cp "${APP_CONFIG}" applications.json
cp "${BENCHMARK_CONFIG}" benchmarks.json
cp "${INTERFERENCE_CONFIG}" interference.json

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

echo "${SOURCE_BASE}/benchmarks/bin/iobench.jar"

# Build temp files and directories for the benchmark
for INSTANCE in `seq ${INSTANCES}`; do
	DIR="${DATA_BASE}/metadata.${INSTANCE}/"
    mkdir -p "${DIR}"
    if [ $? -ne 0 ]; then
        echo "Failed to create ${DIR}"
        exit 6
    fi

	# Clean the directory out if it exists
	rm -f "${DIR}/*"
	if [ $? -ne 0 ]; then
		echo "Failed to clean ${DIR}"
		exit 7
	fi

    FILE="${DATA_BASE}/iobench.${INSTANCE}"
    if [ ! -r "${FILE}" ]; then
        echo "${SOURCE_BASE}/benchmarks/bin"
        java -classpath "${SOURCE_BASE}/benchmarks/bin/iobench.jar" Main create "${FILE}" 256M
        if [ $? -ne 0 ]; then
           echo "Failed to create ${FILE}"
           exit 8
        fi
    fi
done

exit 0
