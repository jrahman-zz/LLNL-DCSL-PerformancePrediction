#!/bin/bash

usage() {
	echo "Usage: main.sh app interference output_path"
}

if [ $# -ne 3 ]; then
	usage
	exit 1
fi

APP_HOME=/p/lscratche/rahman3/apps/
APP_DATA=/p/lscratche/rahman3/app_data/`hostname`/
APP="${1}"
INTERFERENCE="${2}"
OUTPUT_PATH="${3}"
BASE_DIR=$(dirname $0)

INSTANCES=2
CONFIG="${BASE_DIR}/config/config.json"
APP_CONFIG="${BASE_DIR}/config/applications.json"
BENCHMARK_CONFIG="${BASE_DIR}/config/benchmarks.json"
INTERFERENCE_CONFIG="${BASE_DIR}/config/interference.json"

# Perform pre-run setup
"${BASE_DIR}/setup.sh" "${INSTANCES}" "${CONFIG}" "${INTERFERENCE_CONFIG}" "${BENCHMARK_CONFIG}" "${APP_CONFIG}" "${APP_DATA}" "${APP_HOME}"
if [ $? -ne 0 ]; then
	echo "Setup failed"
	exit 2
fi

~/python2/bin/python "${BASE_DIR}/automation/runner/run1.py" --applications "${APP}" --interference "${INTERFERENCE}" --output "${OUTPUT_PATH}"
if [ $? -ne 0 ]; then
   echo "Run failed"
   exit 3
fi

# Cleanup time
"${BASE_DIR}/cleanup.sh" "${INSTANCES}" "${APP_DATA}"
if [ $? -ne 0 ]; then
	echo "Cleanup failed"
	exit 4
fi

exit 0
