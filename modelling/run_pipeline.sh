#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage run_pipeline.sh MULTIAPPDATA"
    exit 1
fi

./prepare_data.py ${1} output xlabels ylabels
if [ $? -ne 0 ]; then
    echo "Error: prepare_data.py failed"
    exit 2
fi

srun -n1 -N1 -c4 -ppdebug "${SPARKHOME}/bin/spark-submit" --master --local[4] als.py output
if [ $? -ne 0 ]; then
    echo "Error als.py failed"
    exit 3
fi

# TODO, final error analysis
