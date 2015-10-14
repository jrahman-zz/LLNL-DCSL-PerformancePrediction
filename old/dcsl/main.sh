#!/bin/bash

usage() {
	echo "Usage: main.sh interference output_path"
}

if [ $# -ne 2 ]; then
	usage
	exit 1
fi

APP_HOME=/p/lscratche/rahman3/apps/
APP_DATA=/p/lscratche/rahman3/app_data/`hostname`/
INTERFERENCE="${1}"
OUTPUT_PATH="${2}"
BASE_DIR=$(dirname $0)


CONFIG="${BASE_DIR}/config/config.json"
APP_CONFIG="${BASE_DIR}/config/applications.json"
BENCHMARK_CONFIG="${BASE_DIR}/config/benchmarks.json"
INTERFERENCE_CONFIG="${BASE_DIR}/config/interference.json.training"

# Perform pre-run setup
"${BASE_DIR}/setup.sh" 2 "${CONFIG}" "${INTERFERENCE_CONFIG}" "${BENCHMARK_CONFIG}" "${APP_CONFIG}" "${APP_DATA}" "${APP_HOME}"
if [ $? -ne 0 ]; then
	echo "Setup failed"
	exit 2
fi

~/python2/bin/python "${BASE_DIR}/automation/runner/run.py" --applications 'all' --interference "${INTERFERENCE}" --output "${OUTPUT_PATH}"
if [ $? -ne 0 ]; then
   echo "Run failed"
   exit 3
fi

exit 0
