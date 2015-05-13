#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Error: Must give benchmark name"
    exit 1
fi

./load.sh ${SPEC_DIR} /tmp/applications/ ${1} train
if [ $? -ne 0 ]; then
    exit 1
fi

./start.sh ${SPEC_DIR} /tmp/applications/ ${1}
if [ $? -ne 0 ]; then
    exit 1
fi

./run.sh ${SPEC_DIR} /tmp/applications/ ${1} train 1
if [ $? -ne 0 ]; then
    exit 1
fi

./stop.sh ${SPEC_DIR} /tmp/applications/
if [ $? -ne 0 ]; then
    exit 1
fi

./cleanup.sh ${SPEC_DIR} /tmp/applications/ ${1}
exit $?
