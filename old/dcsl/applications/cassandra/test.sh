#!/bin/bash

./load.sh ${CASSANDRA_DIR} /tmp/applications/ ${YCSB_DIR} cassandra.pid ./cassandra.in.sh
if [ $? -ne 0 ]; then
    exit 1
fi

./start.sh ${CASSANDRA_DIR} /tmp/applications/ cassandra.pid ./cassandra.in.sh
if [ $? -ne 0 ]; then
    exit 1
fi

./run.sh ${CASSANDRA_DIR} /tmp/applications/ ${YCSB_DIR} 10000
if [ $? -ne 0 ]; then
    exit 1
fi

./stop.sh ${CASSANDRA_DIR} /tmp/applications cassandra.pid
if [ $? -ne 0 ]; then
    exit 1
fi

./cleanup.sh
exit $?
