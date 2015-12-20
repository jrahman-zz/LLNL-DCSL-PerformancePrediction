#!/bin/bash

APPS_DIR=/p/lscratche/${USER}/apps
#MYSQLDIR=$APPS_DIR/mysql-5.1.57
MEMCACHED=$APPS_DIR/memcached
#YCSBDIR=$APPS_DIR/YCSB

#if [ ! -d "$MYSQLDIR" ]; then
#    # Control will enter here if $MYSQLDIR doesn't exist.
#    echo "Error: MySQL missing"
#    exit 1
#fi

CWD=`pwd`

YCSBDIR="${APPS_DIR}/ycsb-0.4.0"

#if [ ! -d "${YCSBDIR}" ]; then
#    wget http://github.com/brianfrankcooper/YCSB/releases/download/0.4.0/ycsb-0.4.0.tar.gz
#    tar -C "${APPS_DIR}" -zxvf ycsb-0.4.0.tar.gz
#    if [ $? -ne 0 ]; then
#        echo "Error: Failed to untar YCSB"
#        exit 1
#    fi
#    rm ycsb-0.4.0.tar.gz
#fi

if [ ! -d "${MEMCACHED}" ]; then
    echo "Installing Memcached at $MEMCACHED/install"
    mkdir -p $MEMCACHED/install
    cd $MEMCACHED
    wget http://memcached.org/files/memcached-1.4.25.tar.gz
    tar xvzf memcached-1.4.25.tar.gz 
    cd memcached-1.4.25
    ./configure --prefix=$MEMCACHED/install
    make
    make install
fi

