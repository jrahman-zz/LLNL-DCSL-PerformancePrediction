#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: run_spark.sh PORT"
    exit 1
fi

PORT=${1}

srun -n1 -N1 -c4 -ppdebug "${SPARKHOME}/bin/spark-submit" --master local[4] run_experiment.py `hostname` ${PORT}
if [ $? -ne 0 ]; then
    echo "Error run_experiment.py failed"
    exit 3
fi
