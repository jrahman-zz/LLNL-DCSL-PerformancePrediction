#!/bin/bash

./load.sh ${MEMCACHED_DIR} /tmp/applications/ memcached.pid 2048
if [ $? -ne 0 ]; then
    exit 1
fi

./start.sh ${MEMCACHED_DIR} /tmp/applications/ memcached.pid 2048 2
if [ $? -ne 0 ]; then
    exit 1
fi

./run.sh ${MEMCACHED_DIR} /tmp/applications/ 10000
if [ $? -ne 0 ]; then
    exit 1
fi

./stop.sh ${MEMCACHED_DIR} /tmp/applications/ memcached.pid
if [ $? -ne 0 ]; then
    exit 1
fi

./cleanup.sh
exit $?
