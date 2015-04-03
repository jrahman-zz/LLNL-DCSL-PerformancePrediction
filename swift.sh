#!/bin/bash


usage() {
	echo "usage: swift.sh name generator_script"
}

if [ $# -ne 2 ]; then
	usage
	exit 1
fi

NAME=$1
CONFIG_SCRIPT=$2
BASE_PATH=$(dirname $0)

echo "Generating run configurations..."

RUN_FILE="${NAME}_run_configurations"
python "${CONFIG_SCRIPT}" "${RUN_FILE}"

if [ $? -ne 0 ]; then
	echo "Run configuration generation failed"
	exit 2
fi

echo "Launching swift in background..."
screen -dmSL "${NAME}" swift -tc.file "${BASE_PATH}/tc.data" -sites.file "${BASE_PATH}/sites.moab.sierra.xml" "${BASE_PATH}/run.swift" -run.file="${RUN_FILE}"

if [ $? -ne 0 ]; then
	echo "Failed to launch swift"
	exit 3
fi

exit 0
