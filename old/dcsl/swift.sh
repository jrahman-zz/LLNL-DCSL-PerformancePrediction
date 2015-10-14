#!/bin/bash


usage() {
	echo "usage: swift.sh name generator_script [background]"
}

if [ $# -lt 2 ]; then
	usage
	exit 1
fi

NAME=$1
CONFIG_SCRIPT=$2
if [ $# -gt 2 ]; then
	BACKGROUND=$3
else
	BACKGROUND=1
fi

BASE_PATH=$(dirname $0)

echo "Generating run configurations..."
RUN_FILE="${NAME}_run_configurations"
python "${CONFIG_SCRIPT}" "${RUN_FILE}"

if [ $? -ne 0 ]; then
	echo "Run configuration generation failed"
	exit 2
fi


CMD="swift -tc.file \"${BASE_PATH}\"/tc.data -sites.file \"${BASE_PATH}/sites.moab.sierra.xml\" \"${BASE_PATH}/run.swift\" -run.file=\"${RUN_FILE}\""

if [ ${BACKGROUND} -eq 1 ]; then
	echo "Launching swift in background..."
	screen -dmSL "${NAME}" ${CMD}
	if [ $? -ne 0 ]; then
		echo "Failed to launch swift"
		exit 3
	fi
	exit 0
else
	echo "Launching swift in foreground..."
	echo ${CMD}
	${CMD}
	exit $? 
fi
