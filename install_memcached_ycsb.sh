#!/bin/bash

APPS_DIR=/p/lscratche/${USER}/apps
MEMCACHED=$APPS_DIR/memcached
YCSBDIR="${APPS_DIR}/YCSB_with_memcache/"

if [ ! -d "${YCSBDIR}" ]; then
    mkdir -p $YCSBDIR
    cd $YCSBDIR
    git clone https://github.com/brianfrankcooper/YCSB.git
    cd YCSB/
    mvn -pl com.yahoo.ycsb:memcached-binding -am clean package
fi

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

