#!/bin/bash

./load.sh ${VOLDEMORT_DIR} /tmp/applications/ ${YCSB_DIR}
if [ $? -ne 0 ]; then
    exit 1
fi

./start.sh ${VOLDEMORT_DIR} /tmp/applications/
if [ $? -ne 0 ]; then
    exit 1
fi

./run.sh ${VOLDEMORT_DIR} /tmp/applications/ ${YCSB_DIR} 10000
if [ $? -ne 0 ]; then
    exit 1
fi

./stop.sh ${VOLDEMORT_DIR} /tmp/applications/
if [ $? -ne 0 ]; then
    exit 1
fi

./cleanup.sh
exit $?
