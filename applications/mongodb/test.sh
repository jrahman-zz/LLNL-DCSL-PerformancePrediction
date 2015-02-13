#!/bin/bash

./load.sh ${YCSB_DIR} ${MONGODB_DIR} /tmp/applications/ `pwd`/mongodb.pid
if [ $? -ne 0 ]; then
    exit 1
fi

./start.sh ${MONGODB_DIR} /tmp/applications/ `pwd`/mongodb.pid
if [ $? -ne 0 ]; then
    exit 1
fi

./run.sh ${YCSB_DIR} 10000
if [ $? -ne 0 ]; then
    exit 1
fi

./stop.sh ${MONGODB_DIR} /tmp/applications/
if [ $? -ne 0 ]; then
    exit 1
fi

./cleanup.sh
exit $?
