#!/bin/bash

if [ $# -ge 1 ]; then
    WORKERS=$1
else
    WORKERS=1
fi

srun -n1 -N1 -c${WORKERS} -ppdebug ./process_experiments.py ${WORKERS}
