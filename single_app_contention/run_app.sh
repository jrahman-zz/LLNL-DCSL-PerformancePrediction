#!/bin/bash

#
# Test for killing a background process
#

TEST_NAME="test_expt"

../bin/time 2>"${TEST_NAME}" | 3>>"${TEST_NAME}" taskset -c 1 perf stat -I 1000 -e cycles,instructions --log-fd=3 -x ' ' ../bin/reporter_33554423 1> "${TEST_NAME}.pid" 2>> "${TEST_NAME}" &
if [ $? -ne 0 ]; then
	echo "Error: Failed to start perf and reporter"
	exit 1
fi
echo "PID: ${BACKGROUND_PID}"
taskset -c 2 parsecmgmt -a run -i native -n 2 -p blackscholes
kill `cat "${TEST_NAME}.pid"`
