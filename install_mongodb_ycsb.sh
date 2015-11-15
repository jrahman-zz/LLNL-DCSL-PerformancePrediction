#!/bin/bash

APPS_DIR=/p/lscratche/${USER}/apps
MONGODIR=$APPS_DIR/mongodb-linux-x86_64-3.0.7
YCSBDIR=$APPS_DIR/YCSB

if [ ! -d "$MONGODIR" ]; then
    # Control will enter here if $MONGODIR doesn't exist.
    echo "Error: MongoDB missing"
    exit 1
fi

CWD=`pwd`

if [ ! -d "$YCSBDIR" ]; then
	  # Control will enter here if $YCSBDIR doesn't exist.
	  cd $APPS_DIR
	  git clone git://github.com/brianfrankcooper/YCSB.git
	  cd YCSB
	  "${CWD}/mvn" -pl \!cassandra2,\!gemfire,\!hbase094,\!hbase098,\!hbase10,\!kudu,\!distribution clean package 
fi
