#!/bin/bash

DATA_DIR=$1

CONFIG_FILE="${DATA_DIR}/redis.config"
REDIS_DIR="/p/lscratche/${USER}/apps/redis-stable"

cp "./apps/redis/redis.config" "${CONFIG_FILE}"
if [ $? -ne 0 ]; then
    exit 1
fi

${REDIS_DIR}/src/redis-server "${CONFIG_FILE}" --dir "${DATA_DIR}" --pidfile "${DATA_DIR}/app.pid" 2>&1 > /dev/null &
REDIS_PID=$!
echo "REDIS-PID: ${REDIS_PID}"
echo "${REDIS_PID}" > "${DATA_DIR}/app.pid"
wait "${REDIS_PID}"
