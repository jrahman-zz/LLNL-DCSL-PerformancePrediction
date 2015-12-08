#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Usage: run_pipeline.sh MULTIAPPDATA PORT"
    exit 1
fi

DATA=${1}
PORT=${2}

./prepare_data.py ${DATA} xlabels ylabels
if [ $? -ne 0 ]; then
    echo "Error: prepare_data.py failed"
    exit 2
fi

# TODO, final error analysis
