#!/bin/bash

#
# Performs cleanup after a given run
#
#
#


usage() {
	echo "Usage: cleanup.sh INSTANCE DATA_BASE"
}

if [ $# -ne 2 ]; then
	usage
	exit 1
fi

INSTANCES=${1}
DATE_BASE=${2}

# Clean up metadata dirs
for INSTANCE in `seq ${INSTANCES}`; do
	DIR="${DATA_BASE}/metadata.${INSTANCE}"
	rm -f "${DIR}/*"
	if [ $? -ne 0 ]; then
		echo "Failed to remove ${DIR}"
		exit 2
	fi
done

exit 0
