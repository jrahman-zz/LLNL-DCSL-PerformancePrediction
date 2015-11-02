#!/bin/bash

APPS_DIR=/p/lscratche/mitra3/apps
MONGODIR=$APPS_DIR/mongodb-linux-x86_64-2.6.7
YCSBDIR=$APPS_DIR/YCSB

if [ ! -d "$MONGODIR" ]; then
	  # Control will enter here if $MONGODIR doesn't exist.
fi

if [ ! -d "$YCSBDIR" ]; then
	  # Control will enter here if $YCSBDIR doesn't exist.
	  cd $APPS_DIR
	  git clone git://github.com/brianfrankcooper/YCSB.git
	  cd YCSB
	  mvn clean package
fi


