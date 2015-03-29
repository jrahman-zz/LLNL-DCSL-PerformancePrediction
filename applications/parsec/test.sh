#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Error: Must give benchmark name"
    exit 1
fi

./load.sh ${PARSEC_DIR} /tmp/applications/ ${1}
if [ $? -ne 0 ]; then
    exit 1
fi

./start.sh ${PARSEC_DIR} /tmp/applications/ ${1}
if [ $? -ne 0 ]; then
    exit 1
fi

./run.sh ${PARSEC_DIR} /tmp/applications/ ${1} simlarge 2
if [ $? -ne 0 ]; then
    exit 1
fi

./stop.sh ${PARSEC_DIR} /tmp/applications/
if [ $? -ne 0 ]; then
    exit 1
fi

./cleanup.sh ${PARSEC_DIR} /tmp/applications/ ${1}
exit $?
