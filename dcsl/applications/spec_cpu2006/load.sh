#!/bin/bash

usage() {
    echo "Usage: load.sh SPEC_DIR DATA_DIR INSTANCE BMARK_NAME SIZE"
}

if [ $# -ne 5 ]; then
    usage
    exit 1
fi

HOSTNAME=`hostname`

BASE_DIR=$(dirname $0)/

# Path
SPEC_DIR=${1}
if [ ! -d "${SPEC_DIR}" ]; then
    echo "Error: SPEC directory doesn't exist"
    usage
    exit 2
fi

if [ ! -x "${SPEC_DIR}/bin/runspec" ]; then
    echo "Error: SPEC directory is incorrect, can't find binary"
    usage
    exit 3
fi

# Path to directory to store data directory
DATA_DIR=${2}
if [ ! -d "${DATA_DIR}" ]; then
    echo "Error: Data parent directory doesn't exist"
    usage
    exit 4
fi

INSTANCE=${3}
BMARK_NAME=${4}

SIZE=${5}
if [ "${SIZE}" != "train" -a "${SIZE}" != "test" -a "${SIZE}" != "ref" ]; then
    echo "Error: Bad size"
    usage
    exit 5
fi

# Delete old datadir
DATA="${DATA_DIR}/spec_data_${BMARK_NAME}_${INSTANCE}"
if [ -d "${DATA}" ]; then
    echo "Load: Deleting old data directory at ${DATA} ..."
    rm -rf "${DATA}"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to delete ${DATA}"
        exit 6
    fi
    echo "Load: Deleted old data directory"
fi

# Create new, empty data directory on target drive
echo "Load: Creating new data directory at ${DATA} ..."
mkdir -p "${DATA}"
if [ $? -ne 0 ]; then
    echo "Error: Failed to create data directory"
    exit 7
fi
echo "Load: Created data directory"

BINARY_NAME=`${BASE_DIR}/read_binary.py "${BASE_DIR}/fake_commands.json" "${BMARK_NAME}"`
if [ $? -ne 0 ]; then
    echo "Error: Failed to load binary name"
    exit 8
fi

# Copy benchmark
BASE_PATH="${SPEC_DIR}/benchspec/CPU2006/${BMARK_NAME}/run"
BINARY_PATH="${BASE_PATH}/build_base_x86-64.0000/${BINARY_NAME}"
RUN_PATH="${BASE_PATH}/run_base_${SIZE}_x86-64.0000"

cp -r "${RUN_PATH}" "${DATA}"
if [ $? -ne 0 ]; then
    echo "Error: Failed to copy application input"
    exit 9
fi

TARGET="${DATA}/run_base_${SIZE}_x86-64.0000/${BINARY_NAME}_base.x86-64"
if [ ! -x "${TARGET}" ]; then
    echo "Load: Binary not found at ${TARGET}, transfering ${BINARY_PATH}"
	cp "${BINARY_PATH}" "${TARGET}"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to copy binary to destination"
        exit 10
    fi
fi

# TODO
#echo "Load: Building benchmark"
#(
#    cd "${SPEC_DIR}"
#    source shrc
#    ./bin/runspec -c custom-linux64.cfg --tune base --noreportable --size ${SIZE} --define HOSTNAME=${HOSTNAME} --define INSTANCE=${INSTANCE} --action setup ${BMARK_NAME}
#)
#if [ $? -ne 0 ]; then
#    echo "Error: Failed to compile benchmark"
#    exit 8
#fi

# Make a 2nd copy of the SPEC benchmark for interference use
#SOURCE="${SPEC_DIR}/benchspec/CPU2006/${BMARK_NAME}/run/run_base_${SIZE}_${HOSTNAME}_${INSTANCE}.0000"
#DEST="${SPEC_DIR}/benchspec/CPU2006/${BMARK_NAME}/run/run_base_${SIZE}_${HOSTNAME}.0001"
#mkdir -p "${DEST}"
#if [ $? -ne 0 ]; then
#	echo "Error: Failed to create new directory"
#	exit 9
#fi

#cp -r "${SOURCE}"/* "${DEST}"
#if [ $? -ne 0 ]; then
#	# Retry once
#	cp -r "${SOURCE}"/* "${DEST}"
#	if [ $? -ne 0 ]; then
#		echo "Error: Failed to duplicate benchmark"
#		exit 10
#	fi
#fi

# Perform a rewrite of rules based on the new directory
#ORIG=run_base_${SIZE}_${HOSTNAME}.0000
#NEW=run_base_${SIZE}_${HOSTNAME}.0001
#sed -i s^${SOURCE}^${DEST}^ "${DEST}"/*.cmd && sed -i s^${ORIG}^${NEW}^ "${DEST}"/*.cmd
#if [ $? -ne 0 ]; then
#	echo "Error: Failed to rewrite run dir"
#	exit 10
#fi

exit 0
