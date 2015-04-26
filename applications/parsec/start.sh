#!/bin/bash


usage() {
    echo "Usage: start.sh PARSEC_DIR DATA_DIR INSTANCE"
}

if [ $# -ne 3 ]; then
	usage
	exit 1
fi

PARSEC_DIR=$1
DATA_DIR=$2
INSTANCE=$3
BMARK_NAME=$4

exit 0
