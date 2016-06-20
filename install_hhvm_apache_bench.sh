#!/bin/bash

use gcc-4.8.5p 

APPS_DIR=/p/lscratche/${USER}/apps
HHVM=$APPS_DIR/hhvm
APACHE_BENCHDIR=$APPS_DIR/AB

if [ ! -d "$HHVN" ]; then
    # Control will enter here if $NGINXDIR doesn't exist.
    mkdir -p $HHVM/install
    #echo "HHVM will be installed in : $HHVM"
    cd $HHVM
    git clone git://github.com/facebook/hhvm.git --depth=1
    cd hhvm
    git submodule update --init --recursive
    which gcc
    #cmake -DMYSQL_UNIX_SOCK_ADDR=/var/run/mysqld/mysqld.sock DESTDIR=$HHVM/install .
    cmake -DMYSQL_UNIX_SOCK_ADDR=/tmp/mysql.sock DESTDIR=$HHVM/install .
    make -j 8
    make install
    echo "Installation of HHVM done"
fi


CWD=`pwd`
exit 1

YCSBDIR="${APPS_DIR}/ycsb-0.3.1"
if [ ! -d "${YCSBDIR}" ]; then
    wget http://github.com/brianfrankcooper/YCSB/releases/download/0.3.1/ycsb-0.3.1.tar.gz
    tar -C "${APPS_DIR}" -zxvf ycsb-0.3.1.tar.gz
    if [ $? -ne 0 ]; then
        echo "Error: Failed to untar YCSB"
        exit 1
    fi
    rm ycsb-0.3.1.tar.gz
fi

#if [ ! -d "$YCSBDIR" ]; then
	  # Control will enter here if $YCSBDIR doesn't exist.
#	  cd $APPS_DIR
#	  git clone git://github.com/brianfrankcooper/YCSB.git
#	  cd YCSB
#	  "${CWD}/mvn" -pl \!cassandra2,\!gemfire,\!hbase094,\!hbase098,\!hbase10,\!kudu,\!distribution clean package 
#fi
