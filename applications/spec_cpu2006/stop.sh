#!/bin/bash

usage() {
    echo "Usage: stop.sh SPEC_DIR DATA_DIR INSTANCE"
}

if [ $# -ne 3 ]; then
    usage
    exit 1
fi

exit 0
