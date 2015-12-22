#!/bin/bash

DATA_DIR=$1

PID_FILE="${DATA_DIR}/app.pid"
ERROR_FILE="${DATA_DIR}/error.log"

NGINX_DIR="/p/lscratche/${USER}/apps/nginx-1.8.0"

$NGINX_DIR/sbin/nginx -c "conf/nginx_non_root.conf" -g "pid ${PID_FILE}; error_log ${ERROR_FILE};"

# Wait for PID file to be populated, if nginx process is HIGHLY delayed there is a non-zero chance for a race
sleep 2

# NGINX will remove it's own PID file for us
while [ -f "${PID_FILE}" ]; do
    sleep 2
done
