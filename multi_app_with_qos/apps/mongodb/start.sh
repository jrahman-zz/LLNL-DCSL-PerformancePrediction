#!/bin/bash

DATA_DIR=$1

MONGO_DIR="/p/lscratche/${USER}/apps/mongodb-linux-x86_64-3.0.7"

if [ ! -d "${DATA_DIR}" ]; then
    echo "Error: No data directory"
    exit 1
fi

${MONGO_DIR}/bin/mongod --dbpath "${DATA_DIR}" --pidfilepath "${DATA_DIR}/app.pid" --quiet 2> /dev/null 1> /dev/null
