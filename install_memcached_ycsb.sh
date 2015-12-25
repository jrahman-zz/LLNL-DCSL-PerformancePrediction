#!/bin/bash

APPS_DIR=/p/lscratche/${USER}/apps
MEMCACHED=$APPS_DIR/memcached
YCSBSOURCE="${APPS_DIR}/YCSB_with_memcache/"
YCSB_VERSION="0.7.0-SNAPSHOT"
YCSBDIR="${APPS_DIR}/ycsb-${YCSB_VERSION}"

if [ ! -d "${YCSBDIR}" ]; then
    mkdir -p $YCSBSOURCE
    cp ycsb.pom ${YCSBSOURCE}
    cp ycsb_distribution.pom ${YCSBSOURCE}
    cd $YCSBSOURCE
    rm -rf YCSB
    git clone https://github.com/brianfrankcooper/YCSB.git
    mv ycsb.pom YCSB/pom.xml
    mv ycsb_distribution.pom YCSB/distribution/pom.xml
    cd YCSB/
    mvn clean package
    cp distribution/target/ycsb-${YCSB_VERSION}.tar.gz "${APPS_DIR}"
    cd "${APPS_DIR}"
    tar -zxvf "ycsb-${YCSB_VERSION}.tar.gz"
fi

if [ ! -d "${YCSBDIR}" ]; then
    echo "ERROR: Failed to install YCSB"
    exit 1
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

