#!/bin/bash

usage() {
	echo "Usage: run.sh apps interference output_path base_dir"
}

if [ $# -ne 4 ]; then
	usage
	exit 1
fi

APPS=$1
INTERFERENCE=$2
OUTPUT_PATH=$3
BASE_DIR=$4

echo "Interference: ${INTERFERENCE}"
echo "Apps: ${APPS}"
echo "Output path: ${OUTPUT_PATH}"
echo "Base directory: ${BASE_DIR}"

echo "Starting run..."
~/python2/bin/python ${BASE_DIR}/run.py --applications "${APPS}" --interference "${INTERFERENCE}" --output ${OUTPUT_PATH} --config "${BASE_DIR}"
if [ $? -ne 0 ]; then
    echo "Run failed"
    exit 8
fi

exit 0
