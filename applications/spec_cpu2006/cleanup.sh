#!/bin/bash

usage() {
    echo "Usage: cleanup.sh SPEC_DIR DATA_DIR INSTANCE BMARK_NAME"
}

if [ $# -ne 4 ]; then
    echo "Error: Invalid arguments"
    usage
    exit 1
fi

HOSTNAME=`hostname`
SPEC_DIR=${1}
INSTANCE=${3}
BMARK_NAME=${4}

# Remove temp dir
DATA_DIR="${2}/spec/${BMARK_DIR}"
if [ -d "${DATA_DIR}" ]; then
    echo "Cleanup: Removing ${DATA_DIR}..."
    rm -rf "${DATA_DIR}"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to cleanup data"
        exit 2
    fi
    echo "Cleanup: Removed ${DATA_DIR}"
fi

# Remove run files

RUN_DIR="${SPEC_DIR}/benchspec/CPU2006/${BMARK_NAME}/"
echo "Cleanup: Checking for ${RUN_DIR}/run/"
if [ -d "${RUN_DIR}/run/" ]; then
    echo "Cleanup: Removing ${RUN_DIR}/run/"
	GONE=0
    for RETRY in `seq 1 10`; do
		rm -rf "${RUN_DIR}"/run/*"${HOSTNAME}_${INSTANCE}"*
    	if [ $? -ne 0 ]; then
        	sleep 5
		else
			GONE=1
			break
		fi
    done
	if [ ${GONE} -ne 1 ]; then
		"Error: Failed to cleanup"
		exit 3
	fi
else
    echo "Error: No run directory found"
    exit 4
fi

exit 0
