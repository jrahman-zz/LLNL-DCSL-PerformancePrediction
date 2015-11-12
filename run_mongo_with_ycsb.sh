#!/bin/bash

#APPS_DIR=/p/lscratche/mitra3/apps
#MONGO_DIR=$APPS_DIR/mongodb-linux-x86_64-2.6.7
#YCSB_DIR=$APPS_DIR/YCSB

#cd $MONGO_DIR
rm -rf /tmp/mongo_dbpath
mkdir /tmp/mongo_dbpath
#./bin/mongod --dbpath /tmp/mongo_dbpath &
mongod --dbpath /tmp/mongo_dbpath &
sleep 60   # sleep for 60 sec, give time mongo db to init

#cd $YCSB_DIR
#./bin/ycsb load mongodb -s -P workloads/workloada > outputLoad.txt
ycsb run mongodb -s -P workloads/workloada | tee outputRun.txt
