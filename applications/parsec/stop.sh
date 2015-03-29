#!/bin/bash

usage() {
    echo "Usage: stop.sh PARSEC_DIR DATA_DIR"
}

if [ $# -ne 2 ]; then
    usage
    exit 1
fi

exit 0
