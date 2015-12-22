#!/bin/bash

DATA_DIR=$1

MEMCACHED_DIR="/p/lscratche/${USER}/apps/memcached/install"

${MEMCACHED_DIR}/bin/memcached -d -m 1024 -u root -l 127.0.0.1 -p 11211 -P "${DATA_DIR}/app.pid"

# Jason: This start script needs to block upon starting the QoS application
# Does the -d flag result in the memcached daemon forking and allowing the script to continue?
# If so a call to wait needs to be added here so this script blocks
# Also, stdout and stderr surpression *might* need to be added
