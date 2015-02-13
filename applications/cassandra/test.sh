#!/bin/bash

./load.sh ${YCSB_DIR} ${CASSANDRA_DIR} /tmp/applications/ cassandra.pid ./cassandra.in.sh
if [ $? -ne 0 ]; then
    exit 1
fi

./start.sh ${CASSANDRA_DIR} /tmp/applications/ cassandra.pid ./cassandra.in.sh
if [ $? -ne 0 ]; then
    exit 1
fi

./run.sh ${YCSB_DIR} 10000
if [ $? -ne 0 ]; then
    exit 1
fi

./stop.sh cassandra.pid
if [ $? -ne 0 ]; then
    exit 1
fi

./cleanup.sh
exit $?
