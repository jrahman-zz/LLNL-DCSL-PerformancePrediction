#!/bin/bash

DATA_DIR=$1

MEMCACHED_DIR="/p/lscratche/${USER}/apps/memcached/install"

${MEMCACHED_DIR}/bin/memcached -u ${USER} -m 1024 -l 127.0.0.1 -p 11211 -P "${DATA_DIR}/app.pid"
