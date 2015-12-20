#!/bin/bash

WORKLOAD=$1
OUTPUT_PATH=$2

# According to ab documentation it only runs 1 thread always. Is that enough to saturate nginx ? Do we need to run multiple ab process?

echo "**** Running Apache bench with Nginx **** with workload = ${WORKLOAD}"
ab -n 50000 -c 1000  http://localhost:8080/ 2> /dev/null  > ${OUTPUT_PATH}
