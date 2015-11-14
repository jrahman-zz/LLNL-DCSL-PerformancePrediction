#!/bin/bash

APPS_DIR=/p/lscratche/mitra3/apps
YCSB_DIR=$APPS_DIR/YCSB

load_or_run=$1
workload=$2

cd $YCSB_DIR

if [ $load_or_run == "load" ]
then
 echo "**** Loading MongoDB with YCSB **** with workload = $workload"
 ./bin/ycsb $load_or_run mongodb -s -P $workload
elif [ $load_or_run == "run" ]
then
 echo "**** Running MongoDB with YCSB **** with workload = $workload"
./bin/ycsb $load_or_run mongodb -s -P $workload
fi
